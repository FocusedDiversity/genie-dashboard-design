#!/usr/bin/env python3
"""Publish a dashboard's HELIX record (dashboards/<slug>/docs/helix/) to an Azure DevOps project wiki.

The repo stays the source of truth. The wiki gets a read-only copy of the documentation artifacts only: one
subpage per artifact under a parent page, plus a generated overview on the parent page. Dashboard JSON, SQL,
spikes, and source files are never copied; links to them become links to the file in the repo. Run it when
Deploy is recorded and again at every Iterate close. Each run rebuilds the managed pages from the repo, so
edits made in the wiki are overwritten.

How it works:
  - A project wiki is a git repo (`<Project>.wiki`, branch `wikiMaster`), so the script clones it and
    pushes. Git credentials that work for the code repo work here too, with no Wiki REST API scope needed.
  - Pages:
    - <wiki-path>.md is the overview.
    - <wiki-path>/<NN-Activity-Artifact>.md holds one artifact each.
    - <wiki-path>/.order sets the subpage order. Unmanaged pages already in the folder are kept, after the
      managed ones.
  - Links:
    - Relative links between HELIX artifacts become wiki page links.
    - Every other relative link (SQL baselines, dataset files, the .lvdash.json) becomes a link to the file
      in the Azure DevOps repo at --branch.
  - Mockup (optional, --include-mockup):
    - The wiki cannot run the HTML, so docs/helix/02-design/screenshots/*.png (one per tab, named
      NN-<tab>.png, in tab order) are copied to the wiki's /.attachments and shown on a "02 Design Mockup"
      page that links to the HTML in the repo.
    - Off by default; when used, capture the screenshots from the current mockup first.
  - Safety:
    - It refuses to publish uncommitted HELIX changes (the wiki must match a repo commit) unless
      --allow-dirty is given.
    - It refuses to publish a HEAD that isn't on origin/<branch> (repo links would not resolve) unless
      --allow-unpushed is given.
    - It refuses to overwrite a non-empty parent page it did not create unless --force is given.
    - --dry-run shows the change set without committing.

Per-dashboard settings live in dashboards/<slug>/docs/helix/wiki-publish.json, so a run needs only --slug:
    {"title": "...", "wiki_path": "Space/Dashboards/My-Dashboard", "dashboard_url": "...", "include_mockup": false}
The wiki git URL and repo web URL are derived from `origin` (Azure DevOps). The link branch is the current
branch. Any key may be overridden on the command line.

Usage (from the working repo root; see assets/wiki-publish.md for the HELIX step):
    python publish_wiki.py --slug my_dashboard --init --title "My Dashboard" --wiki-path Space/Dashboards/My-Dashboard [--dashboard-url URL]
    python publish_wiki.py --slug my_dashboard --dry-run
    python publish_wiki.py --slug my_dashboard [--commit-trailer "Co-authored-by: ..."]
    overrides: [--title T] [--wiki-path P] [--dashboard-url U] [--wiki-repo URL] [--repo-web URL] [--branch B]
               [--wiki-branch wikiMaster] [--workdir DIR] [--include-mockup] [--allow-dirty] [--allow-unpushed] [--force]
"""
import argparse
import hashlib
import json
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

MARKER = "<!-- helix-sync:managed -->"
PAGES = [  # (wiki page file stem, source relative to docs/helix, what it holds)
    ("01-Frame-Dashboard-Brief", "01-frame/dashboard-brief.md", "Purpose, personas, sources, and each cycle's scope"),
    ("01-Frame-Widget-Inventory", "01-frame/widget-inventory.md", "Every widget (W-###) and each cycle's changes"),
    ("02-Design-Decisions", "02-design/design-decisions.md", "Theme, aggregation and grain rules, filters, layout"),
    ("02-Design-Mockup", None, "Screenshots of the current mockup, one per tab"),
    ("02-Design-Definitions", "02-design/definitions-review.md", "Every metric and dimension definition"),
    ("03-Test-Widget-Test-Plan", "03-test/widget-test-plan.md", "Baselines (T-###) and expected values"),
    ("04-Build-Prompt-Catalog", "04-build/prompt-catalog.md", "Build specs per widget and checks run"),
    ("05-Deploy-Deployment-Guide", "05-deploy/deployment-guide.md", "Releases, live checks, verification, rollback"),
    ("06-Iterate-Iteration-Log", "06-iterate/iteration-log.md", "Change log, feedback, drift, parking lot"),
    ("06-Iterate-Stakeholder-Inputs", "06-iterate/stakeholder-inputs.md", "Every question asked and decision made"),
]
LINK = re.compile(r"(!?)\[((?:[^\]\[]|\[[^\]]*\])*)\]\((<[^>]+>|[^)\s]+)(\s+\"[^\"]*\")?\)")


def run(cmd, cwd=None, check=True):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and p.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd)}\n{p.stdout}\n{p.stderr}")
    return p.stdout.strip()


def repo_url(a, rel, anchor=""):
    q = urllib.parse.urlencode({"path": "/" + rel, "version": "GB" + a.branch}, quote_via=urllib.parse.quote)
    return f"{a.repo_web}?{q}" + (f"&anchor={urllib.parse.quote(anchor)}" if anchor else "")


def wiki_link(a, stem, anchor=""):
    return "/" + a.wiki_path.strip("/") + "/" + stem + (f"#{anchor}" if anchor else "")


def rewrite_links(a, text, src_rel, page_by_src):
    """src_rel: the artifact's path relative to the repo root (posix)."""
    base = posixpath.dirname(src_rel)

    def sub(m):
        bang, label, target, title = m.group(1), m.group(2), m.group(3), m.group(4) or ""
        t = target[1:-1] if target.startswith("<") else target
        if re.match(r"^([a-z]+:|#|/)", t, re.I):
            return m.group(0)
        path, _, anchor = t.partition("#")
        rel = posixpath.normpath(posixpath.join(base, urllib.parse.unquote(path)))
        if rel.startswith(".."):
            return m.group(0)
        if not bang and rel in page_by_src:
            return f"[{label}]({wiki_link(a, page_by_src[rel], anchor)}{title})"
        return f"{bang}[{label}]({repo_url(a, rel, anchor)}{title})"

    return LINK.sub(sub, text)


def banner(a, src_rel, sha, today):
    src = f"[`{src_rel}`]({repo_url(a, src_rel)})" if src_rel else "the repo"
    return (f"{MARKER}\n> **Generated from the repo**: {src} as of commit `{sha}` ({today}, branch `{a.branch}`). "
            f"Edit the repo file, not this page; the next HELIX sync overwrites wiki edits.\n\n")


def overview(a, helix, sha, today, published, shots_attached):
    brief = (helix / "01-frame/dashboard-brief.md").read_text(encoding="utf-8") if (helix / "01-frame/dashboard-brief.md").exists() else ""
    status = next((l for l in brief.splitlines() if l.startswith("**Status**")), "")
    log = (helix / "06-iterate/iteration-log.md").read_text(encoding="utf-8") if (helix / "06-iterate/iteration-log.md").exists() else ""
    cycles = [int(n) for n in re.findall(r"^## Cycle (\d+)\b", log, re.M)]
    out = [banner(a, f"dashboards/{a.slug}/docs/helix/", sha, today), f"# {a.title}: HELIX record", ""]
    if status:
        out += [status, ""]
    if a.dashboard_url:
        out += [f"**Dashboard**: [{a.title}]({a.dashboard_url})", ""]
    if cycles:
        out += [f"**Latest cycle in the iteration log**: Cycle {max(cycles)}; see [Iteration Log]({wiki_link(a, '06-Iterate-Iteration-Log')}).", ""]
    out += ["This page and its subpages are a read-only copy of the dashboard's HELIX record: Frame, Design, Test, Build, Deploy, and Iterate. "
            "Each activity ends in a stakeholder-approved gate, and every widget traces from W-### (Frame) to T-### (Test) to a verified "
            "Deploy outcome.", "", "| Page | What it holds |", "|---|---|"]
    for stem, src, what in PAGES:
        if stem in published:
            out.append(f"| [{stem.replace('-', ' ')}]({wiki_link(a, stem)}) | {what} |")
    if shots_attached:
        out += ["", f"![{a.title} mockup]({shots_attached[0]})"]
    return "\n".join(out) + "\n"


CONFIG = "wiki-publish.json"


def derive_from_origin(root):
    """Azure DevOps origin -> (repo web URL, project wiki git URL). Returns (None, None) for other hosts."""
    url = run(["git", "remote", "get-url", "origin"], cwd=root, check=False)
    m = re.match(r"^https://(?:([^@/]+)@)?dev\.azure\.com/([^/]+)/([^/]+)/_git/([^/?#]+)", url)
    if not m:
        return None, None
    user, org, project, repo = m.groups()
    web = f"https://dev.azure.com/{org}/{project}/_git/{repo}"
    wiki_name = urllib.parse.quote(urllib.parse.unquote(project).replace(" ", "-") + ".wiki")
    wiki = f"https://{user + '@' if user else ''}dev.azure.com/{org}/{project}/_git/{wiki_name}"
    return web, wiki


def settings(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--init", action="store_true", help=f"write docs/helix/{CONFIG} from --title / --wiki-path / --dashboard-url and exit")
    for k in ("title", "wiki-path", "dashboard-url", "wiki-repo", "repo-web", "branch", "wiki-branch"):
        ap.add_argument("--" + k)
    ap.add_argument("--workdir")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true", help="publish even if the HELIX record has uncommitted changes")
    ap.add_argument("--allow-unpushed", action="store_true", help="publish even if HEAD is not on the remote branch")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--include-mockup", action="store_true", help="also publish 02-design/screenshots/*.png as a mockup page")
    ap.add_argument("--commit-trailer", help="extra line appended to the wiki commit message, e.g. a Co-authored-by trailer")
    a = ap.parse_args(argv)

    a.root = Path(run(["git", "rev-parse", "--show-toplevel"]))
    a.helix_rel = f"dashboards/{a.slug}/docs/helix"
    a.helix = a.root / a.helix_rel
    if not a.helix.is_dir():
        sys.exit(f"no HELIX record at {a.helix}")
    cfg_path = a.helix / CONFIG
    if a.init:
        if not (a.title and a.wiki_path):
            sys.exit("--init needs --title and --wiki-path (the parent wiki page, e.g. Team-Space/Dashboards/My-Dashboard)")
        cfg = {"title": a.title, "wiki_path": a.wiki_path.strip("/"), "dashboard_url": a.dashboard_url or "", "include_mockup": False}
        cfg_path.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8", newline="\n")
        sys.exit(f"wrote {cfg_path}; commit it, then run: python publish_wiki.py --slug {a.slug} --dry-run")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    for k in ("title", "wiki_path", "dashboard_url", "wiki_repo", "repo_web", "branch", "wiki_branch"):
        if getattr(a, k) is None and cfg.get(k):
            setattr(a, k, cfg[k])
    a.include_mockup = a.include_mockup or bool(cfg.get("include_mockup"))
    web, wiki = derive_from_origin(a.root)
    a.repo_web = a.repo_web or web
    a.wiki_repo = a.wiki_repo or wiki
    a.branch = a.branch or run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=a.root)
    a.wiki_branch = a.wiki_branch or "wikiMaster"
    missing = [k for k in ("title", "wiki_path", "repo_web", "wiki_repo") if not getattr(a, k)]
    if missing:
        sys.exit(f"missing {', '.join(missing)}: run --init first, or pass them (no {CONFIG} at {cfg_path})")
    a.wiki_path = a.wiki_path.strip("/")
    return a


def main():
    a = settings()
    root, helix_rel, helix = a.root, a.helix_rel, a.helix
    dirty = run(["git", "status", "--porcelain", "--", helix_rel], cwd=root)
    if dirty and not a.allow_dirty:
        sys.exit(f"uncommitted HELIX changes; commit and push first (or --allow-dirty):\n{dirty}")
    if not a.allow_unpushed:
        run(["git", "fetch", "-q", "origin", a.branch], cwd=root, check=False)
        on_remote = subprocess.run(["git", "merge-base", "--is-ancestor", "HEAD", f"origin/{a.branch}"], cwd=root).returncode == 0
        if not on_remote:
            sys.exit(f"HEAD is not on origin/{a.branch}; push first so the wiki's repo links resolve (or --allow-unpushed)")
    sha, today = run(["git", "log", "-1", "--format=%h %cs", "--", helix_rel], cwd=root).split()
    print(f"publishing {helix_rel} @ {sha} ({a.branch}) -> {a.wiki_path} on {a.wiki_branch}")

    work = Path(a.workdir) if a.workdir else Path(tempfile.gettempdir()) / ("helix-wiki-" + hashlib.sha1(a.wiki_repo.encode()).hexdigest()[:8])
    if (work / ".git").is_dir():
        run(["git", "fetch", "--depth", "1", "origin", a.wiki_branch], cwd=work)
        run(["git", "reset", "--hard", f"origin/{a.wiki_branch}"], cwd=work)
    else:
        run(["git", "-c", "core.longpaths=true", "-c", "core.autocrlf=false", "clone", "--depth", "1", "--branch", a.wiki_branch,
             "--config", "core.autocrlf=false", "--config", "core.longpaths=true", a.wiki_repo, str(work)])
    run(["git", "config", "core.longpaths", "true"], cwd=work)
    run(["git", "config", "core.autocrlf", "false"], cwd=work)
    if run(["git", "status", "--porcelain"], cwd=work):
        run(["git", "reset", "-q", "--hard", f"origin/{a.wiki_branch}"], cwd=work)

    parent_md = work / (a.wiki_path + ".md")
    folder = work / a.wiki_path
    if parent_md.exists():
        cur = parent_md.read_text(encoding="utf-8").strip()
        if cur and MARKER not in cur and not a.force:
            sys.exit(f"{parent_md.name} has content not written by this sync; use --force to replace it")
    folder.mkdir(parents=True, exist_ok=True)

    page_by_src = {f"{helix_rel}/{src}": stem for stem, src, _ in PAGES if src and (helix / src).exists()}
    published = []
    for stem, src, _ in PAGES:
        if src is None:
            continue
        p = helix / src
        if not p.exists():
            continue
        src_rel = f"{helix_rel}/{src}"
        body = rewrite_links(a, p.read_text(encoding="utf-8"), src_rel, page_by_src)
        (folder / f"{stem}.md").write_text(banner(a, src_rel, sha, today) + body, encoding="utf-8", newline="\n")
        published.append(stem)

    shots = sorted((helix / "02-design/screenshots").glob("*.png")) if a.include_mockup and (helix / "02-design/screenshots").is_dir() else []
    attached = []
    if shots:
        att = work / ".attachments"
        att.mkdir(exist_ok=True)
        lines = [banner(a, f"{helix_rel}/02-design/screenshots/", sha, today), f"# {a.title}: mockup", "",
                 f"Interactive version: [`dashboard-mockup.html`]({repo_url(a, helix_rel + '/02-design/dashboard-mockup.html')}) "
                 "(download it and open it in a browser). The screenshots below are one per tab, taken from that file.", ""]
        for s in shots:
            name = f"helix-{a.slug}-{s.name}"
            shutil.copyfile(s, att / name)
            attached.append(f"/.attachments/{name}")
            tab = re.sub(r"^\d+-", "", s.stem).replace("-", " ").title()
            lines += [f"## {tab}", "", f"![{tab}](/.attachments/{name})", ""]
        (folder / "02-Design-Mockup.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
        published.append("02-Design-Mockup")

    parent_md.write_text(overview(a, helix, sha, today, published, attached), encoding="utf-8", newline="\n")
    managed = [stem for stem, _, _ in PAGES if stem in published]
    existing = (folder / ".order").read_text(encoding="utf-8").split() if (folder / ".order").exists() else []
    others = [s for s in existing if s not in managed and (folder / f"{s}.md").exists()]
    (folder / ".order").write_text("\n".join(managed + others) + "\n", encoding="utf-8", newline="\n")

    own = [parent_md, folder / ".order"] + [folder / f"{s}.md" for s in managed] + [work / a_.lstrip("/") for a_ in attached]
    run(["git", "add", "--"] + [p.relative_to(work).as_posix() for p in own], cwd=work)
    changes = run(["git", "diff", "--cached", "--name-status"], cwd=work)
    stray = [l for l in run(["git", "status", "--porcelain"], cwd=work).splitlines() if not l.startswith(("M ", "A ", "D ", "R "))]
    if stray:
        sys.exit("wiki clone has changes outside the managed pages; nothing committed:\n" + "\n".join(stray[:20]))
    print(changes or "no changes")
    if not changes or a.dry_run:
        print("dry run: nothing committed" if a.dry_run else "wiki already up to date")
        return
    msg = ["-m", f"HELIX sync: {a.title} ({a.slug}) @ {sha}"] + (["-m", a.commit_trailer] if a.commit_trailer else [])
    run(["git", "commit", "-q"] + msg, cwd=work)
    run(["git", "push", "origin", a.wiki_branch], cwd=work)
    print("pushed", run(["git", "rev-parse", "--short", "HEAD"], cwd=work), "to", a.wiki_branch, "| pages:", len(managed), "| images:", len(attached))


if __name__ == "__main__":
    main()
