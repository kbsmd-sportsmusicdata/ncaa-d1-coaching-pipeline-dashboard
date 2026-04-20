#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


DEFAULT_SPORTS = {
    "womens basketball": "Women's Basketball",
    "women's basketball": "Women's Basketball",
    "womens soccer": "Women's Soccer",
    "women's soccer": "Women's Soccer",
    "womens softball": "Women's Softball",
    "women's softball": "Women's Softball",
    "womens volleyball": "Women's Volleyball",
    "women's volleyball": "Women's Volleyball",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Filter NCAA D1 womens sports parquet down to basketball, soccer, softball, and volleyball."
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to ncaa_d1_womens_sports.parquet",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where filtered outputs should be written.",
    )
    parser.add_argument(
        "--sports",
        nargs="+",
        default=[
            "Women's Basketball",
            "Women's Soccer",
            "Women's Softball",
            "Women's Volleyball",
        ],
        help="Sports to keep. Defaults to basketball, soccer, softball, volleyball.",
    )
    parser.add_argument(
        "--emit-eda-bundle",
        action="store_true",
        help="Also write an EDA-ready bundle with teams.csv, players.csv, and an EDA manifest.",
    )
    parser.add_argument(
        "--bundle-profile",
        default="generic",
        help="Profile name to place in the EDA manifest when --emit-eda-bundle is used.",
    )
    return parser.parse_args()


def normalize_sport_value(value: object) -> str:
    text = str(value).strip().lower()
    text = text.replace("’", "'")
    return text


def canonicalize_requested_sports(values: list[str]) -> dict[str, str]:
    canonical: dict[str, str] = {}
    for value in values:
        key = normalize_sport_value(value)
        canonical[key] = value.strip()
    for key, value in DEFAULT_SPORTS.items():
        canonical.setdefault(key, value)
    return canonical


def sort_columns(df: pd.DataFrame) -> list[str]:
    preferred = [
        "division",
        "sport",
        "year",
        "group_type",
        "role",
        "staff_level",
        "gender",
        "race_ethnicity_normalized",
        "race_ethnicity_raw",
        "count",
    ]
    ordered = [col for col in preferred if col in df.columns]
    ordered += [col for col in df.columns if col not in ordered]
    return ordered


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"Input parquet not found: {args.input}")

    df = pd.read_parquet(args.input)
    if "sport" not in df.columns:
        raise RuntimeError("The input parquet must contain a 'sport' column.")

    requested = canonicalize_requested_sports(args.sports)
    requested_keys = set(requested.keys())

    sport_norm = df["sport"].map(normalize_sport_value)
    filtered = df.loc[sport_norm.isin(requested_keys)].copy()

    if filtered.empty:
        raise RuntimeError(
            "No rows matched the requested sports. "
            f"Requested={sorted(requested.values())}"
        )

    # Preserve the original sport names, but tidy whitespace.
    filtered["sport"] = filtered["sport"].astype(str).str.strip()
    filtered = filtered[sort_columns(filtered)]

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    filtered_parquet = output_dir / "ncaa_d1_womens_sports_filtered.parquet"
    filtered_csv = output_dir / "ncaa_d1_womens_sports_filtered.csv"
    summary_json = output_dir / "filter_summary.json"

    filtered.to_parquet(filtered_parquet, index=False)
    filtered.to_csv(filtered_csv, index=False)

    sport_counts = (
        filtered["sport"]
        .astype(str)
        .value_counts(dropna=False)
        .sort_index()
        .to_dict()
    )

    summary = {
        "schema_version": "ncaa_d1_womens_sports_filter_v1",
        "generated_at_utc": timestamp,
        "input_path": str(args.input.resolve()),
        "output_dir": str(output_dir.resolve()),
        "rows_before": int(len(df)),
        "rows_after": int(len(filtered)),
        "sports_requested": sorted(requested.values()),
        "sports_kept": sport_counts,
        "outputs": {
            "filtered_parquet": str(filtered_parquet.resolve()),
            "filtered_csv": str(filtered_csv.resolve()),
        },
    }
    summary_json.write_text(json.dumps(summary, indent=2))

    if args.emit_eda_bundle:
        bundle_dir = output_dir / "eda_bundle"
        bundle_dir.mkdir(parents=True, exist_ok=True)

        # The current EDA Agent v2 expects a teams.csv + players.csv bundle.
        # For this parquet-shaped coaching dataset, we emit the filtered table twice
        # so the generic profile can consume it without changing the agent first.
        teams_csv = bundle_dir / "teams.csv"
        players_csv = bundle_dir / "players.csv"
        teams_parquet = bundle_dir / "teams.parquet"
        players_parquet = bundle_dir / "players.parquet"
        manifest_path = bundle_dir / "eda_agent.manifest.json"

        filtered.to_csv(teams_csv, index=False)
        filtered.to_csv(players_csv, index=False)
        filtered.to_parquet(teams_parquet, index=False)
        filtered.to_parquet(players_parquet, index=False)

        manifest = {
            "source_root": str(bundle_dir.resolve()),
            "dataset_label": "ncaa_d1_womens_sports_filtered",
            "dataset_version": timestamp,
            "profile_name": args.bundle_profile,
            "teams_path": "teams.csv",
            "players_path": "players.csv",
            "extra_files": {
                "filtered_csv": "ncaa_d1_womens_sports_filtered.csv",
                "filtered_parquet": "ncaa_d1_womens_sports_filtered.parquet",
                "filter_summary": "filter_summary.json",
            },
        }
        (bundle_dir / "ncaa_d1_womens_sports_filtered.csv").write_text(filtered_csv.read_text())
        filtered.to_parquet(bundle_dir / "ncaa_d1_womens_sports_filtered.parquet", index=False)
        (bundle_dir / "filter_summary.json").write_text(summary_json.read_text())
        manifest_path.write_text(json.dumps(manifest, indent=2))

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
