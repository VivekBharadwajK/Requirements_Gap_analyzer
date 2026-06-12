#!/usr/bin/env python3
"""
Requirements Gap Analysis Agent

Processes business and engineering team transcripts using a CrewAI
multi-agent pipeline to identify gaps between requirements and solutions.

Usage:
    python main.py --business ./transcripts/business \\
                   --engineering ./transcripts/engineering \\
                   --output report.json

    python main.py --business ./transcripts/business \\
                   --engineering ./transcripts/engineering \\
                   --output report.md --format markdown
"""
import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict

from dotenv import load_dotenv

load_dotenv()

from crew import run_gap_analysis_crew
from file_loader import load_transcripts
from report_formatter import format_report


def run_pipeline(
    business_dir: str,
    engineering_dir: str,
    output_path: str,
    output_format: str = "json",
) -> None:
    """
    Run the gap analysis pipeline.

    Steps:
    1. Load transcripts from both directories
    2. Execute the CrewAI crew
    3. Format and write the report
    """
    print("=" * 60)
    print("  Requirements Gap Analysis Agent")
    print("=" * 60)
    print()

    # Step 1: Load transcripts
    print("[1/3] Loading transcripts...")
    business_transcripts = load_transcripts(business_dir)
    engineering_transcripts = load_transcripts(engineering_dir)
    print(f"      Found {len(business_transcripts)} business transcript(s)")
    print(f"      Found {len(engineering_transcripts)} engineering transcript(s)")
    print()

    if not business_transcripts and not engineering_transcripts:
        print("Error: No transcripts found. Nothing to analyse.")
        sys.exit(1)

    if not business_transcripts:
        print("Error: No business transcripts found. Cannot extract requirements.")
        sys.exit(1)

    if not engineering_transcripts:
        print("Warning: No engineering transcripts. All requirements will be flagged as unaddressed.")
        # Create empty engineering list — the gap agent will flag everything
        engineering_transcripts = []

    # Step 2: Run the Agentic pipeline
    print("[2/3] Running the analysis pipeline...")
    print()

    requirements, solutions, gaps = run_gap_analysis_crew(
        business_transcripts=business_transcripts,
        engineering_transcripts=engineering_transcripts,
    )

    print()
    print(f"      Extracted {len(requirements)} requirement(s)")
    print(f"      Extracted {len(solutions)} solution(s)")
    print(f"      Identified {len(gaps)} gap(s)")
    print()

    # Step 3: Format and write report
    print("[3/3] Writing report...")
    report_content = format_report(requirements, solutions, gaps, output_format)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report_content, encoding="utf-8")
    print(f"      Report written to: {output_path}")
    print()

    # Summary
    print("=" * 60)
    print("  Analysis Complete")
    print("=" * 60)
    print(f"  Requirements: {len(requirements)}")
    print(f"  Solutions:    {len(solutions)}")
    print(f"  Gaps:         {len(gaps)}")

    if gaps:
        high = sum(1 for g in gaps if g.get("severity") == "high")
        medium = sum(1 for g in gaps if g.get("severity") == "medium")
        low = sum(1 for g in gaps if g.get("severity") == "low")
        print(f"    - High:   {high}")
        print(f"    - Medium: {medium}")
        print(f"    - Low:    {low}")
    print()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description=(
            "Requirements Gap Analysis Agent — "
            "Identifies gaps between business requirements and engineering plans."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --business ./transcripts/business --engineering ./transcripts/engineering --output report.json
  python main.py --business ./transcripts/business --engineering ./transcripts/engineering --output report.md --format markdown
        """,
    )

    parser.add_argument(
        "--business",
        required=True,
        help="Directory containing business team transcript files (.txt or .md)",
    )
    parser.add_argument(
        "--engineering",
        required=True,
        help="Directory containing engineering team transcript files (.txt or .md)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path for the gap report",
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="json",
        help="Output format: 'json' (default) or 'markdown'",
    )

    args = parser.parse_args()

    # Display configuration
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    print(f"Using Ollama model: {model}")
    print(f"Ollama URL: {base_url}")
    print()

    # Run the pipeline
    try:
        run_pipeline(args.business, args.engineering, args.output, args.format)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
