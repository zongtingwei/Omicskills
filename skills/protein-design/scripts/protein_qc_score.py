#!/usr/bin/env python3
"""Score protein-design metrics with shared QC thresholds."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable


STANDARD_THRESHOLDS = {
    "pLDDT": 0.85,
    "pTM": 0.70,
    "ipTM": 0.50,
    "PAE_interaction": 12.0,
    "scRMSD": 2.0,
    "shape_complementarity": 0.50,
    "interface_dG": -10.0,
    "instability_index": 40.0,
    "GRAVY": 0.40,
    "esm2_pll_normalized": 0.0,
}

STRINGENT_THRESHOLDS = {
    "pLDDT": 0.90,
    "pTM": 0.80,
    "ipTM": 0.60,
    "PAE_interaction": 10.0,
    "scRMSD": 1.5,
    "shape_complementarity": 0.60,
    "interface_dG": -15.0,
    "instability_index": 30.0,
    "GRAVY": 0.20,
    "esm2_pll_normalized": 0.2,
}

ALIASES = {
    "pLDDT": ["pLDDT", "plddt"],
    "pTM": ["pTM", "ptm"],
    "ipTM": ["ipTM", "iptm"],
    "PAE_interaction": ["PAE_interaction", "pae_interaction", "iPAE", "ipae"],
    "scRMSD": ["scRMSD", "scrmsd", "self_consistency_rmsd"],
    "shape_complementarity": ["shape_complementarity", "SC", "sc"],
    "interface_dG": ["interface_dG", "dG", "interface_dg"],
    "instability_index": ["instability_index", "instability"],
    "GRAVY": ["GRAVY", "gravy"],
    "esm2_pll_normalized": ["esm2_pll_normalized", "pll", "esm_pll"],
    "cysteine_count": ["cysteine_count", "num_cys"],
}

WEIGHTS = {
    "pLDDT": 0.30,
    "ipTM": 0.20,
    "PAE_interaction": 0.20,
    "shape_complementarity": 0.15,
    "esm2_pll_normalized": 0.15,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path, help="CSV containing one row per design.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Where to write the scored CSV. Defaults to <input>.scored.csv",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Use the stringent QC thresholds instead of the standard thresholds.",
    )
    return parser.parse_args()


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader)


def find_value(row: dict[str, str], canonical_name: str) -> float | None:
    for name in ALIASES[canonical_name]:
        raw = row.get(name)
        if raw is None or raw == "":
            continue
        try:
            return float(raw)
        except ValueError:
            return None
    return None


def bool_to_str(flag: bool) -> str:
    return "TRUE" if flag else "FALSE"


def pass_lower_is_better(value: float | None, threshold: float) -> bool:
    return value is not None and value < threshold


def pass_higher_is_better(value: float | None, threshold: float) -> bool:
    return value is not None and value > threshold


def normalized_score(metric: str, value: float | None, thresholds: dict[str, float]) -> float:
    if value is None:
        return 0.0
    if metric == "PAE_interaction":
        return max(0.0, min(1.0, 1.0 - (value / 20.0)))
    if metric == "shape_complementarity":
        return max(0.0, min(1.0, value))
    if metric == "esm2_pll_normalized":
        floor = thresholds[metric]
        return max(0.0, min(1.0, value - floor + 0.5))
    return max(0.0, min(1.0, value))


def score_row(row: dict[str, str], thresholds: dict[str, float]) -> dict[str, str]:
    values = {metric: find_value(row, metric) for metric in ALIASES}

    structural_pass = all(
        [
            pass_higher_is_better(values["pLDDT"], thresholds["pLDDT"]),
            values["scRMSD"] is None or pass_lower_is_better(values["scRMSD"], thresholds["scRMSD"]),
            values["pTM"] is None or pass_higher_is_better(values["pTM"], thresholds["pTM"]),
        ]
    )
    binding_pass = all(
        [
            values["ipTM"] is None or pass_higher_is_better(values["ipTM"], thresholds["ipTM"]),
            values["PAE_interaction"] is None or pass_lower_is_better(values["PAE_interaction"], thresholds["PAE_interaction"]),
            values["shape_complementarity"] is None
            or pass_higher_is_better(values["shape_complementarity"], thresholds["shape_complementarity"]),
            values["interface_dG"] is None or pass_lower_is_better(values["interface_dG"], thresholds["interface_dG"]),
        ]
    )

    even_cysteines = values["cysteine_count"] is None or int(values["cysteine_count"]) % 2 == 0
    expression_pass = all(
        [
            values["instability_index"] is None
            or pass_lower_is_better(values["instability_index"], thresholds["instability_index"]),
            values["GRAVY"] is None or pass_lower_is_better(values["GRAVY"], thresholds["GRAVY"]),
            values["esm2_pll_normalized"] is None
            or pass_higher_is_better(values["esm2_pll_normalized"], thresholds["esm2_pll_normalized"]),
            even_cysteines,
        ]
    )

    composite_score = 0.0
    for metric, weight in WEIGHTS.items():
        composite_score += weight * normalized_score(metric, values[metric], thresholds)

    qc_pass = structural_pass and binding_pass and expression_pass

    result = dict(row)
    result.update(
        {
            "pass_structural": bool_to_str(structural_pass),
            "pass_binding": bool_to_str(binding_pass),
            "pass_expression": bool_to_str(expression_pass),
            "pass_qc": bool_to_str(qc_pass),
            "composite_score": f"{composite_score:.4f}",
        }
    )
    return result


def summarize(rows: Iterable[dict[str, str]]) -> str:
    rows = list(rows)
    if not rows:
        return "No rows found in input CSV."

    total = len(rows)
    structural = sum(r["pass_structural"] == "TRUE" for r in rows)
    binding = sum(r["pass_binding"] == "TRUE" for r in rows)
    expression = sum(r["pass_expression"] == "TRUE" for r in rows)
    final = sum(r["pass_qc"] == "TRUE" for r in rows)

    lines = [
        f"Designs scored: {total}",
        f"Structural pass rate: {structural}/{total} ({structural / total:.1%})",
        f"Binding pass rate: {binding}/{total} ({binding / total:.1%})",
        f"Expression pass rate: {expression}/{total} ({expression / total:.1%})",
        f"Overall QC pass rate: {final}/{total} ({final / total:.1%})",
    ]
    return "\n".join(lines)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    args = parse_args()
    thresholds = STRINGENT_THRESHOLDS if args.strict else STANDARD_THRESHOLDS
    input_rows = load_rows(args.input_csv)
    scored_rows = [score_row(row, thresholds) for row in input_rows]
    scored_rows.sort(key=lambda row: float(row["composite_score"]), reverse=True)
    for rank, row in enumerate(scored_rows, start=1):
        row["rank"] = str(rank)

    output_path = args.output or args.input_csv.with_suffix(".scored.csv")
    write_rows(output_path, scored_rows)
    print(summarize(scored_rows))
    print(f"Wrote scored table to {output_path}")


if __name__ == "__main__":
    main()
