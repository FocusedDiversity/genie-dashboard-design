#!/usr/bin/env python3
"""Structural summary of a Tableau .twb or .twbx workbook.

Used by the genie-dashboard-design HELIX workflow's Tableau intake (see
tableau-intake.md). Grepping the raw XML for structural tags is fragile on
real workbooks: attribute order on <dashboard>/<zone>/<connection> varies
between files (sometimes `name` is the first attribute, sometimes the
third), and a workbook-wide list of calculated fields is usually far too
large to review one by one (real workbooks commonly carry hundreds, most of
them formatting/parameter/filter helpers, not metrics). This parses the XML
properly with the standard library (no install required) and reports the
scoped view that actually matters for mining:

  - dashboards: name + which worksheet zones are placed on it
  - worksheets: mark class(es), rows/cols shelf, encodings (shelf -> field),
    and that worksheet's OWN <datasource-dependencies> entries (caption,
    role, formula) -- Tableau re-declares only the fields a worksheet
    actually uses there, which is the practical unit to mine one widget from
  - datasources: the live/original connection (if any) plus, separately, a
    packaged <extract>'s connection (a workbook can have both: a live
    definition kept for "refresh from source", and the extract actually
    shipped in the .twbx)
  - calculated fields: deduplicated by internal id, classified simple vs.
    LOD (`{FIXED/INCLUDE/EXCLUDE...}`) vs. table-calc (LOOKUP/WINDOW_/
    RUNNING_/INDEX/RANK/TOTAL/PREVIOUS_VALUE), with which worksheets
    reference each one -- only LOD/table-calc ones are worth a
    [NEEDS CLARIFICATION] marker; simple ones (including the common
    string/boolean/parameter-comparison helpers that drive filters, not
    metrics) are SQL-translatable directly and don't need one

Usage:
    python list_workbook_structure.py <path-to.twb-or.twbx> [--worksheet NAME]

--worksheet limits worksheet and calculated-field output to just that one
worksheet, useful once you already know which worksheet you're mining.
"""
import argparse
import json
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

LOD_MARKERS = ("{FIXED", "{INCLUDE", "{EXCLUDE")
TABLE_CALC_MARKERS = (
    "LOOKUP(", "WINDOW_", "RUNNING_", "INDEX(", "RANK(", "TOTAL(", "PREVIOUS_VALUE(",
)


def load_twb(path: Path) -> ET.Element:
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            twb_names = [n for n in zf.namelist() if n.lower().endswith(".twb")]
            if not twb_names:
                raise ValueError(f"No .twb file found inside {path}")
            with zf.open(twb_names[0]) as f:
                return ET.parse(f).getroot()
    return ET.parse(path).getroot()


def classify_formula(formula):
    if not formula:
        return "simple"
    if any(marker in formula for marker in LOD_MARKERS):
        return "lod"
    if any(marker in formula for marker in TABLE_CALC_MARKERS):
        return "table_calc"
    return "simple"


def describe_connection(conn):
    if conn is None:
        return None
    return {
        "class": conn.get("class"),
        "server": conn.get("server"),
        "dbname": conn.get("dbname"),
        "filename": conn.get("filename"),
    }


def collect_datasources(root):
    out = []
    for ds in root.findall("./datasources/datasource"):
        name = ds.get("name")
        if name == "Parameters":
            continue
        entry = {"name": name, "caption": ds.get("caption") or name}

        top_conn = ds.find("./connection")
        if top_conn is not None and top_conn.get("class") == "federated":
            inner = top_conn.find(".//named-connection/connection")
            entry["source_connection"] = describe_connection(inner if inner is not None else top_conn)
        else:
            entry["source_connection"] = describe_connection(top_conn)

        extract_conn = ds.find("./extract/connection")
        if extract_conn is not None:
            entry["packaged_extract"] = describe_connection(extract_conn)
        else:
            entry["packaged_extract"] = None

        out.append(entry)
    return out


def collect_dashboards(root):
    out = []
    for dash in root.findall(".//dashboards/dashboard"):
        zone_names = sorted({z.get("name") for z in dash.findall(".//zone") if z.get("name")})
        out.append({"name": dash.get("name"), "worksheet_zones": zone_names})
    return out


def collect_worksheets(root, only_name, calc_index):
    out = []
    for ws in root.findall(".//worksheets/worksheet"):
        name = ws.get("name")
        if only_name and name != only_name:
            continue

        panes = ws.findall(".//panes/pane")
        marks = sorted({m.get("class") for p in panes for m in p.findall(".//mark") if m.get("class")})
        encodings = []
        for p in panes:
            enc = p.find(".//encodings")
            if enc is not None:
                for child in enc:
                    encodings.append({"shelf": child.tag, "field": child.get("column")})

        rows = ws.find(".//table/rows")
        cols = ws.find(".//table/cols")

        deps = []
        for dep_block in ws.findall(".//datasource-dependencies"):
            for col in dep_block.findall("column"):
                calc = col.find("calculation")
                formula = calc.get("formula") if calc is not None else None
                deps.append(
                    {
                        "name": col.get("name"),
                        "caption": col.get("caption"),
                        "role": col.get("role"),
                        "formula": formula,
                    }
                )
                if formula:
                    idx = calc_index.setdefault(
                        col.get("name"),
                        {
                            "caption": col.get("caption"),
                            "formula": formula,
                            "classification": classify_formula(formula),
                            "worksheets": set(),
                        },
                    )
                    idx["worksheets"].add(name)

        out.append(
            {
                "name": name,
                "mark_classes": marks,
                "rows_shelf": rows.text if rows is not None else None,
                "cols_shelf": cols.text if cols is not None else None,
                "encodings": encodings,
                "datasource_dependencies": deps,
            }
        )
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("workbook", help="Path to a .twb or .twbx file")
    parser.add_argument("--worksheet", help="Limit worksheet/calculated-field output to one worksheet by name")
    args = parser.parse_args()

    root = load_twb(Path(args.workbook))

    calc_index = {}
    result = {
        "dashboards": collect_dashboards(root),
        "datasources": collect_datasources(root),
        "worksheets": collect_worksheets(root, args.worksheet, calc_index),
    }

    flagged = [
        {
            "name": calc_name,
            "caption": info["caption"],
            "formula": info["formula"],
            "classification": info["classification"],
            "worksheets": sorted(info["worksheets"]),
        }
        for calc_name, info in calc_index.items()
        if info["classification"] != "simple"
    ]
    result["calculated_fields_flagged"] = flagged
    result["calculated_fields_summary"] = {
        "total_referenced": len(calc_index),
        "flagged_lod_or_table_calc": len(flagged),
    }

    print(json.dumps(result, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
