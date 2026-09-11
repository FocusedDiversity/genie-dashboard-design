#!/usr/bin/env python3
"""Read schema, row counts, and a sample from a Tableau .hyper extract.

Used by the genie-dashboard-design HELIX workflow's Tableau workbook intake
(see tableau-intake.md) to confirm the real columns, types, and grain a
.twbx's packaged extract contains, instead of trusting the .twb XML's
declared schema on faith — the same role DESCRIBE/LIMIT 1 plays for a live
warehouse table.

Requires the `tableauhyperapi` package: pip install tableauhyperapi

Usage:
    python read_hyper_schema.py <path-to-file.hyper> [--sample N]

Output: JSON on stdout, one entry per table found in the extract:
    {"tables": [{"name": ..., "row_count": ..., "columns": [...], "sample_rows": [...]}]}
A table-level "error" key means that one table failed to read; it does not
stop the rest from being reported.
"""
import argparse
import json
import sys


def read_hyper_schema(hyper_path: str, sample: int) -> dict:
    from tableauhyperapi import Connection, HyperProcess, Telemetry

    result = {"tables": []}
    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(endpoint=hyper.endpoint, database=hyper_path) as connection:
            catalog = connection.catalog
            for schema_name in catalog.get_schema_names():
                for table_name in catalog.get_table_names(schema=schema_name):
                    try:
                        table_def = catalog.get_table_definition(table_name)
                        columns = [
                            {
                                "name": col.name.unescaped,
                                "type": str(col.type),
                                "nullable": col.nullability.name,
                            }
                            for col in table_def.columns
                        ]
                        row_count = connection.execute_scalar_query(
                            f"SELECT COUNT(*) FROM {table_name}"
                        )
                        sample_rows = []
                        if sample > 0:
                            rows = connection.execute_query(
                                f"SELECT * FROM {table_name} LIMIT {sample}"
                            )
                            sample_rows = [[str(value) for value in row] for row in rows]
                        result["tables"].append(
                            {
                                "name": str(table_name),
                                "row_count": row_count,
                                "columns": columns,
                                "sample_rows": sample_rows,
                            }
                        )
                    except Exception as exc:
                        result["tables"].append({"name": str(table_name), "error": str(exc)})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "hyper_path",
        help="Path to the .hyper file, after unzipping the .twbx (see list_workbook_structure.py's "
        "packaged_extract.dbname for its relative path -- it is not always under Data/Extracts/)",
    )
    parser.add_argument("--sample", type=int, default=5, help="Rows to sample per table (0 to skip)")
    args = parser.parse_args()

    try:
        output = read_hyper_schema(args.hyper_path, args.sample)
    except ImportError:
        print(json.dumps({"error": "tableauhyperapi is not installed. Run: pip install tableauhyperapi"}))
        return 1
    except Exception as exc:
        print(json.dumps({"error": f"Could not open {args.hyper_path}: {exc}"}))
        return 1

    print(json.dumps(output, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
