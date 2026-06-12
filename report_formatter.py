"""
Report formatter — converts gap analysis output to JSON or Markdown.
"""
import json
from typing import List, Dict, Any
from datetime import datetime


def format_report(
    requirements: List[Dict[str, Any]],
    solutions: List[Dict[str, Any]],
    gaps: List[Dict[str, Any]],
    output_format: str = "json",
) -> str:
    """
    Format the full analysis report.
    
    Args:
        requirements: Extracted requirements as dicts
        solutions: Extracted solutions as dicts
        gaps: Gap analysis results as dicts
        output_format: "json" or "markdown"
    
    Returns:
        Formatted report string
    """
    report = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_requirements": len(requirements),
            "total_solutions": len(solutions),
            "total_gaps": len(gaps),
            "gaps_by_type": _count_by_field(gaps, "type"),
            "gaps_by_severity": _count_by_field(gaps, "severity"),
        },
        "requirements": requirements,
        "solutions": solutions,
        "gaps": gaps,
    }

    if output_format == "markdown":
        return _to_markdown(report)
    return json.dumps(report, indent=2)


def _count_by_field(items: List[Dict], field: str) -> Dict[str, int]:
    """Count items by a specific field value."""
    counts: Dict[str, int] = {}
    for item in items:
        value = item.get(field, "unknown")
        counts[value] = counts.get(value, 0) + 1
    return counts


def _to_markdown(report: Dict[str, Any]) -> str:
    """Convert the report to a readable Markdown format."""
    lines = []
    meta = report["metadata"]

    lines.append("# Requirements Gap Analysis Report")
    lines.append("")
    lines.append(f"**Generated:** {meta['generated_at']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Requirements Extracted | {meta['total_requirements']} |")
    lines.append(f"| Solutions Identified | {meta['total_solutions']} |")
    lines.append(f"| **Gaps Found** | **{meta['total_gaps']}** |")
    lines.append("")

    if meta["gaps_by_severity"]:
        lines.append("### Gaps by Severity")
        lines.append("")
        for severity, count in sorted(meta["gaps_by_severity"].items()):
            lines.append(f"- **{severity.upper()}**: {count}")
        lines.append("")

    if meta["gaps_by_type"]:
        lines.append("### Gaps by Type")
        lines.append("")
        for gap_type, count in sorted(meta["gaps_by_type"].items()):
            lines.append(f"- {gap_type.replace('_', ' ').title()}: {count}")
        lines.append("")

    # Gaps section
    lines.append("---")
    lines.append("")
    lines.append("## Gaps")
    lines.append("")

    for gap in report["gaps"]:
        severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
            gap.get("severity", ""), "⚪"
        )
        gap_type = gap.get("type", "unknown").replace("_", " ").upper()
        lines.append(
            f"### {gap.get('gap_id', 'GAP-???')} {severity_icon} [{gap_type}]"
        )
        lines.append("")
        lines.append(f"**Description:** {gap.get('description', 'N/A')}")
        lines.append("")

        req_refs = gap.get("requirement_refs", [])
        sol_refs = gap.get("solution_refs", [])
        if req_refs:
            lines.append(f"**Requirements:** {', '.join(req_refs)}")
        if sol_refs:
            lines.append(f"**Solutions:** {', '.join(sol_refs)}")
        lines.append("")
        lines.append(
            f"**Suggested Action:** {gap.get('suggested_action', 'N/A')}"
        )
        lines.append("")
        lines.append("---")
        lines.append("")

    # Requirements section
    lines.append("## Extracted Requirements")
    lines.append("")
    for req in report["requirements"]:
        lines.append(f"### {req['id']} — {req.get('statement', 'N/A')}")
        lines.append(f"- **Priority:** {req.get('priority', 'unclear')}")
        lines.append(f"- **Raised by:** {req.get('raised_by', 'unknown')}")
        lines.append(
            f"- **Source:** {req.get('source_transcript', 'unknown')}"
        )
        constraints = req.get("constraints", [])
        if constraints:
            lines.append(f"- **Constraints:** {'; '.join(constraints)}")
        if req.get("implicit"):
            lines.append("- *(Implicit requirement)*")
        lines.append("")

    # Solutions section
    lines.append("## Extracted Solutions")
    lines.append("")
    for sol in report["solutions"]:
        lines.append(f"### {sol['id']} — {sol.get('statement', 'N/A')}")
        techs = sol.get("technologies", [])
        if techs:
            lines.append(f"- **Technologies:** {', '.join(techs)}")
        limitations = sol.get("scope_limitations", [])
        if limitations:
            lines.append(f"- **Scope Limitations:** {'; '.join(limitations)}")
        deferred = sol.get("deferred", [])
        if deferred:
            lines.append(f"- **Deferred:** {'; '.join(deferred)}")
        assumptions = sol.get("assumptions", [])
        if assumptions:
            lines.append(f"- **Assumptions:** {'; '.join(assumptions)}")
        lines.append(
            f"- **Source:** {sol.get('source_transcript', 'unknown')}"
        )
        lines.append("")

    return "\n".join(lines)
