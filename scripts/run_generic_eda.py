#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a lightweight generic EDA pass.")
    parser.add_argument("--input", type=Path, required=True, help="Input parquet or CSV")
    parser.add_argument("--output-dir", type=Path, required=True, help="Output directory")
    parser.add_argument("--top-n", type=int, default=10, help="Top-N categories to report")
    return parser.parse_args()


def load_frame(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix in {".csv", ".tsv"}:
        sep = "\t" if suffix == ".tsv" else ","
        return pd.read_csv(path, sep=sep)
    raise ValueError(f"Unsupported input type: {path.suffix}")


def safe_value_counts(df: pd.DataFrame, col: str, top_n: int) -> list[dict[str, object]]:
    if col not in df.columns:
        return []
    counts = (
        df[col]
        .astype("string")
        .fillna("<missing>")
        .value_counts(dropna=False)
        .head(top_n)
    )
    return [{"value": idx, "count": int(val)} for idx, val in counts.items()]


def build_findings(df: pd.DataFrame, top_n: int) -> list[dict[str, object]]:
    findings: list[dict[str, object]] = []

    if "sport" in df.columns:
        sport_counts = df["sport"].astype("string").fillna("<missing>").value_counts()
        if not sport_counts.empty:
            top_sport = sport_counts.index[0]
            findings.append(
                {
                    "title": "Largest sport segment",
                    "insight": f"{top_sport} has the most rows in the filtered dataset.",
                    "evidence": {"sport": str(top_sport), "rows": int(sport_counts.iloc[0])},
                }
            )

    if "year" in df.columns:
        year_counts = df["year"].astype("string").fillna("<missing>").value_counts()
        if not year_counts.empty:
            findings.append(
                {
                    "title": "Most represented year",
                    "insight": f"Year {year_counts.index[0]} appears most often in the filtered data.",
                    "evidence": {"year": str(year_counts.index[0]), "rows": int(year_counts.iloc[0])},
                }
            )

    for col in ["group_type", "role", "staff_level", "gender", "sport_grouping"]:
        counts = safe_value_counts(df, col, 1)
        if counts:
            findings.append(
                {
                    "title": f"Dominant {col.replace('_', ' ')}",
                    "insight": f"The most common {col.replace('_', ' ')} value is {counts[0]['value']}.",
                    "evidence": counts[0],
                }
            )

    missing = df.isna().mean().sort_values(ascending=False)
    if not missing.empty:
        top_missing = missing.head(1)
        col = top_missing.index[0]
        findings.append(
            {
                "title": "Highest missingness",
                "insight": f"{col} has the highest missing rate in the filtered table.",
                "evidence": {"column": col, "missing_rate": float(top_missing.iloc[0])},
            }
        )

    return findings[: max(5, min(10, len(findings)))]


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"Input not found: {args.input}")

    df = load_frame(args.input)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    profile = {
        "input_path": str(args.input.resolve()),
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "generated_at_utc": timestamp,
    }

    if "sport" in df.columns:
        profile["sport_counts"] = (
            df["sport"].astype("string").fillna("<missing>").value_counts(dropna=False).to_dict()
        )
    if "year" in df.columns:
        profile["year_counts"] = (
            df["year"].astype("string").fillna("<missing>").value_counts(dropna=False).to_dict()
        )

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if numeric_cols:
        profile["numeric_summary"] = df[numeric_cols].describe().replace({pd.NA: None}).to_dict()

    missingness = df.isna().mean().sort_values(ascending=False)
    profile["top_missingness"] = [
        {"column": col, "missing_rate": float(rate)}
        for col, rate in missingness.head(args.top_n).items()
    ]

    findings = build_findings(df, args.top_n)
    summary_md = output_dir / "generic_eda_report.md"
    summary_json = output_dir / "generic_eda_summary.json"

    md_lines = [
        "# Generic EDA Report",
        "",
        f"- Input: `{args.input}`",
        f"- Rows: `{len(df)}`",
        f"- Columns: `{len(df.columns)}`",
        "",
        "## Top Findings",
    ]
    for idx, finding in enumerate(findings, 1):
        md_lines.extend(
            [
                f"{idx}. **{finding['title']}**",
                f"   - {finding['insight']}",
                f"   - Evidence: `{json.dumps(finding['evidence'])}`",
            ]
        )
    md_lines.extend(["", "## Missingness", ""])
    for item in profile["top_missingness"]:
        md_lines.append(f"- {item['column']}: {item['missing_rate']:.2%}")

    summary_md.write_text("\n".join(md_lines))
    summary_json.write_text(
        json.dumps(
            {
                "schema_version": "generic_eda_v1",
                "profile": profile,
                "findings": findings,
            },
            indent=2,
        )
    )

    print(json.dumps({"output_dir": str(output_dir.resolve()), "rows": len(df), "findings": len(findings)}, indent=2))


if __name__ == "__main__":
    main()
