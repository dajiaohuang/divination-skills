"""Shared fail-closed CLI for a single Vedic structural lineage."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from systems.vedic_astrology.calculator.engine import (
    VedicAstrologyError,
    calculate_chart,
)


def run_lineage_cli(lineage: str, description: str) -> int:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("input", nargs="?", help="JSON input path; stdin when omitted")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        payload = (
            json.loads(Path(args.input).read_text(encoding="utf-8"))
            if args.input
            else json.load(sys.stdin)
        )
        if not isinstance(payload, dict):
            raise VedicAstrologyError(
                "invalid_input", "The input document must be a JSON object."
            )
        payload["lineages"] = [lineage]
        print(
            json.dumps(
                calculate_chart(payload),
                ensure_ascii=False,
                indent=2 if args.pretty else None,
            )
        )
        return 0
    except (OSError, json.JSONDecodeError, VedicAstrologyError) as exc:
        code = getattr(exc, "code", "invalid_input")
        print(
            json.dumps(
                {"error": {"code": code, "message": str(exc)}},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2
