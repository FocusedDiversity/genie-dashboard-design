# Publish to Wiki (HELIX step)

Copies a dashboard's HELIX **documentation** to an Azure DevOps project wiki so people who don't read the repo
can follow it. It is the last step of **05 Deploy** (end of a build) and of **06 Iterate** (end of a cycle),
for every dashboard that has a `docs/helix/wiki-publish.json`. Dashboards without that file skip the step.

The repo stays the source of truth. The wiki is a read-only copy, rebuilt from the repo on every run.

## What gets published

| Wiki page | Source (`dashboards/<slug>/docs/helix/`) |
|---|---|
| `<wiki_path>` (overview: status, dashboard link, page list) | generated from `01-frame/dashboard-brief.md` and `06-iterate/iteration-log.md` |
| `01 Frame Dashboard Brief` | `01-frame/dashboard-brief.md` |
| `01 Frame Widget Inventory` | `01-frame/widget-inventory.md` |
| `02 Design Decisions` | `02-design/design-decisions.md` |
| `02 Design Definitions` | `02-design/definitions-review.md` (when present) |
| `03 Test Widget Test Plan` | `03-test/widget-test-plan.md` |
| `04 Build Prompt Catalog` | `04-build/prompt-catalog.md` |
| `05 Deploy Deployment Guide` | `05-deploy/deployment-guide.md` |
| `06 Iterate Iteration Log` | `06-iterate/iteration-log.md` |
| `06 Iterate Stakeholder Inputs` | `06-iterate/stakeholder-inputs.md` |

**Documentation only.**
- **Never copied**: the dashboard `.lvdash.json`, dataset or baseline SQL, spikes, the mockup HTML, and stakeholder source files. Relative links to them become links to the file in the Azure DevOps repo at the current branch.
- **Links between artifacts** become wiki page links.
- **Mockup screenshots** are opt-in (`"include_mockup": true`, with `02-design/screenshots/NN-<tab>.png`).

Every page starts with a banner naming its source file and repo commit: "Edit the repo file, not this page."

## One-time setup per dashboard

1. **Pick the parent page.** Use an existing empty wiki page, or a new path; the script creates the folders.
   - The path is the wiki's folder path with spaces as hyphens, e.g. `Data-Analytics-Methodology/Dashboards/Scheduling-Performance`.
   - It is visible in the page's URL or under "Copy page path".
2. **Write the config** from the working repo root:

   ```
   python .claude/skills/genie-dashboard-design/assets/publish_wiki.py --slug <slug> --init \
       --title "<Dashboard Name>" --wiki-path <Parent/Page/Path> --dashboard-url <published dashboard URL>
   ```

   This writes `dashboards/<slug>/docs/helix/wiki-publish.json`. Commit it with the record.
3. **Nothing else to configure.**
   - The wiki git URL and the repo URL are derived from `origin`. A project wiki is the git repo `<Project-Name>.wiki`, branch `wikiMaster`.
   - Links point at the current branch.
   - Put any override (`wiki_repo`, `repo_web`, `branch`, `wiki_branch`) in the config.

## The step (end of Deploy, end of Iterate)

1. **Commit and push the HELIX record first.** The script refuses uncommitted HELIX changes or a HEAD that is not on `origin/<branch>`, because the wiki must match a commit whose links resolve.
2. **Dry run**: `python .claude/skills/genie-dashboard-design/assets/publish_wiki.py --slug <slug> --dry-run`. It lists the pages it would add or change.
3. **Publish**: the same command without `--dry-run`. When an agent runs it, add `--commit-trailer "Co-authored-by: …"` per its commit rules.
4. **Report to the stakeholder** the wiki commit it printed ("pushed `<sha>`" or "wiki already up to date") and the page link.
   - Do **not** write the wiki commit back into the HELIX artifacts. That would make the record dirty and need another sync.
   - The wiki's own git history is the record.

Run it again whenever a HELIX change is committed between cycles. It is repeatable: an unchanged record pushes nothing.

## Rules

- **The repo is the source of truth.** Wiki edits are overwritten on the next sync. Feedback written on the wiki goes into the iteration log, not the page.
- **Branch links**: pages link to the branch they were published from. After the feature branch merges, publish again from `main` so the links survive the branch's deletion.
- **Unmanaged pages** under the parent are kept, listed after the managed pages in `.order`.
- **Parent page guard**: a parent page with content the sync didn't write is never overwritten without `--force`. Confirm with the page owner first.
- **Review before the first publish**: the wiki may have a wider audience than the repo. Check the record for names, internal analyses, or source-document titles that shouldn't be shared more widely.

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `uncommitted HELIX changes` | Commit (and push) the record first |
| `HEAD is not on origin/<branch>` | `git push` first |
| `has content not written by this sync` | The parent page was hand-written; confirm with its owner, then `--force` |
| Clone shows files "deleted" or the checkout fails on Windows | Long attachment paths in the wiki; the script sets `core.longpaths`. If a manual clone failed, run `git config core.longpaths true` and `git restore --source=HEAD :/` |
| 401 / 403 on push | The account needs Contribute on the wiki. The Wiki REST API is not used, so a code-scoped token is enough |
| Wiki API returns 401 with the same token | Expected for code-scoped tokens; the script uses git, not the Wiki API |
