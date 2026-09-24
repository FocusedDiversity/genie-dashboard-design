#!/usr/bin/env python3
"""Structural summary of a Databricks Lakeview dashboard (.lvdash.json).

Used by the genie-dashboard-design HELIX workflow's Lakeview intake (see
lakeview-intake.md), which mines an already-live dashboard into a widget
inventory instead of inventing one. Reading the raw JSON is impractical --
a real dashboard is thousands of lines, most of it per-widget encoding and
formatting detail that doesn't change what the widget *is*. This reports
the scoped view that matters for mining:

  - pages: display name + widget count, in dashboard order
  - widgets: the stable `name` (the id a W-### binds to), widget type,
    resolved title, the dataset(s) it reads, its fields, and its grid
    position -- one row per widget, in reading order (top-to-bottom,
    left-to-right)
  - datasets: name, display name, the calculated columns declared on them,
    and (with --sql) the full query text
  - theme: the dashboard's current `uiSettings.theme`, which is the "before"
    state a restyle is measured against

Two shapes need care and are handled here: a widget's title is sometimes a
bare string and sometimes a `{"value": ...}` object, and text widgets carry
`multilineTextboxSpec` with no `widgetType` at all (these are the section
headers, which carry the page's visual structure but no data).

Usage:
    python list_dashboard_structure.py --list [ROOT]
    python list_dashboard_structure.py <path-to.lvdash.json> [--sql] [--page NAME]

--list discovers candidate dashboards under ROOT (default: current
directory) so the stakeholder can pick one; it skips vendored copies of
this skill and its bundled theme seeds, which are not dashboards anyone
wants to restyle.
"""
import argparse
import json
import sys
from pathlib import Path

# Vendored skill copies carry seed.<theme>.lvdash.json files that are starter
# templates, not dashboards; offering them as candidates is always wrong.
SKIP_DIRS = {".github", ".claude", ".agents", ".git", "node_modules", "__pycache__"}
SKIP_PREFIXES = ("seed.",)


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def discover(root: Path):
    found = []
    for path in sorted(root.rglob("*.lvdash.json")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name.startswith(SKIP_PREFIXES):
            continue
        found.append(path)
    return found


def widget_title(spec: dict) -> str:
    """Title is a bare string in some widget versions, {"value": ...} in others."""
    title = spec.get("frame", {}).get("title")
    if isinstance(title, dict):
        return title.get("value", "") or ""
    return title or ""


def widget_rows(page: dict):
    """One record per widget, in reading order."""
    rows = []
    for item in page.get("layout", []):
        widget = item.get("widget", {})
        pos = item.get("position", {})
        spec = widget.get("spec", {})

        if "multilineTextboxSpec" in widget:
            lines = widget["multilineTextboxSpec"].get("lines", [])
            rows.append({
                "name": widget.get("name", ""),
                "type": "text",
                "title": " ".join(lines)[:120],
                "datasets": [],
                "fields": [],
                "pos": pos,
            })
            continue

        datasets, fields = [], []
        for query in widget.get("queries", []):
            q = query.get("query", {})
            if q.get("datasetName"):
                datasets.append(q["datasetName"])
            fields.extend(f.get("name", "") for f in q.get("fields", []))

        rows.append({
            "name": widget.get("name", ""),
            "type": spec.get("widgetType", "unknown"),
            "title": widget_title(spec),
            "datasets": sorted(set(datasets)),
            "fields": fields,
            "pos": pos,
        })

    rows.sort(key=lambda r: (r["pos"].get("y", 0), r["pos"].get("x", 0)))
    return rows


def fmt_pos(pos: dict) -> str:
    return (f"x{pos.get('x', '?')} y{pos.get('y', '?')} "
            f"{pos.get('width', '?')}x{pos.get('height', '?')}")


def report(path: Path, show_sql: bool, only_page: str | None):
    doc = load(path)
    pages = doc.get("pages", [])
    datasets = doc.get("datasets", [])

    print(f"DASHBOARD: {path}")
    total = sum(len(p.get("layout", [])) for p in pages)
    print(f"{len(pages)} pages, {total} widgets, {len(datasets)} datasets\n")

    print("== THEME (uiSettings.theme) - the 'before' state ==")
    theme = doc.get("uiSettings", {}).get("theme")
    if theme:
        print(json.dumps(theme, indent=2))
    else:
        print("(none set - dashboard uses the Lakeview default theme)")
    print()

    print("== PAGES ==")
    for i, page in enumerate(pages, 1):
        print(f"{i}. {page.get('displayName', '(untitled)')}  "
              f"[name={page.get('name', '')}, {len(page.get('layout', []))} widgets]")
    print()

    for page in pages:
        display = page.get("displayName", "(untitled)")
        if only_page and only_page.lower() not in display.lower():
            continue
        print(f"== WIDGETS - {display} ==")
        for row in widget_rows(page):
            print(f"  [{row['name']}] {row['type']}")
            if row["title"]:
                print(f"      title:    {row['title']}")
            if row["datasets"]:
                print(f"      dataset:  {', '.join(row['datasets'])}")
            if row["fields"]:
                print(f"      fields:   {', '.join(row['fields'])}")
            print(f"      position: {fmt_pos(row['pos'])}")
        print()

    print("== DATASETS ==")
    for ds in datasets:
        print(f"  [{ds.get('name', '')}] {ds.get('displayName', '')}")
        for col in ds.get("columns", []):
            desc = col.get("description", "")
            expr = col.get("expression", "")
            print(f"      column: {col.get('displayName', '')}"
                  + (f" - {desc}" if desc else "")
                  + (f"  [{expr}]" if expr else ""))
        if show_sql:
            sql = "".join(ds.get("queryLines", []))
            print("      query:")
            for line in sql.splitlines():
                print(f"        {line}")
        print()
    if not show_sql and datasets:
        print("(re-run with --sql for full dataset query text)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", nargs="?", help="Path to a .lvdash.json file")
    parser.add_argument("--list", nargs="?", const=".", metavar="ROOT",
                        help="Discover candidate dashboards under ROOT (default: .)")
    parser.add_argument("--sql", action="store_true", help="Include dataset query text")
    parser.add_argument("--page", metavar="NAME", help="Limit widget output to one page")
    args = parser.parse_args()

    if args.list is not None:
        root = Path(args.list)
        if not root.is_dir():
            print(f"Not a directory: {root}", file=sys.stderr)
            return 1
        found = discover(root)
        if not found:
            print(f"No .lvdash.json files found under {root.resolve()}")
            return 0
        print(f"{len(found)} candidate dashboards under {root.resolve()}:\n")
        for path in found:
            try:
                doc = load(path)
                pages = doc.get("pages", [])
                widgets = sum(len(p.get("layout", [])) for p in pages)
                detail = f"{len(pages)} pages, {widgets} widgets, {len(doc.get('datasets', []))} datasets"
            except (json.JSONDecodeError, OSError) as exc:
                detail = f"UNREADABLE: {exc}"
            print(f"  {path}")
            print(f"      {detail}")
        return 0

    if not args.path:
        parser.error("give a .lvdash.json path, or --list to discover them")
    path = Path(args.path)
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 1
    report(path, args.sql, args.page)
    return 0


if __name__ == "__main__":
    sys.exit(main())
