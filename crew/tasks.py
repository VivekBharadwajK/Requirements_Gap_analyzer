"""
Task definitions for the gap analysis pipeline.

"""
from crewai import Task, Agent
from typing import List, Dict

from models import RequirementsList, SolutionsList, GapReport


def create_requirements_task(
    agent: Agent,
    transcripts: List[Dict[str, str]],
) -> Task:
    """
    The requirements extraction task.
    
    Args:
        agent: The requirements analyst agent
        transcripts: List of dicts with 'filename' and 'content' keys
    
    Returns:
        CrewAI Task configured for requirements extraction
    """
    # Combine all transcripts into a single input block
    transcript_text = _format_transcripts(transcripts)

    description = f"""Analyse the following business team meeting transcripts and extract ALL requirements discussed.

For each requirement, identify:
- A unique ID (REQ-001, REQ-002, etc.)
- A concise requirement statement
- Priority: "must-have", "nice-to-have", or "unclear"
- Any constraints (SLAs, compliance rules, geographic scope, timelines)
- The speaker/role who raised it
- Whether it's implicit (implied but not explicitly stated)
- Source transcript filename

Important rules:
- Extract EVERY requirement, including ones mentioned casually or indirectly
- A requirement like "it has to be GDPR compliant" means data handling, consent, right to erasure, etc.
- When a client says "at minimum X" — X is must-have; anything beyond is nice-to-have
- If speakers disagree or contradict, capture both versions and mark priority as "unclear"
- Don't invent requirements not discussed or clearly implied

TRANSCRIPTS:
{transcript_text}"""

    return Task(
        description=description,
        expected_output=(
            "A structured JSON object with a 'requirements' array containing "
            "all extracted requirements, each with id, statement, priority, "
            "constraints, raised_by, implicit, and source_transcript fields."
        ),
        agent=agent,
        output_json=RequirementsList,
    )


def create_solutions_task(
    agent: Agent,
    transcripts: List[Dict[str, str]],
) -> Task:
    """
    The solutions extraction task.
    
    Args:
        agent: The solutions analyst agent
        transcripts: List of dicts with 'filename' and 'content' keys
    
    Returns:
        CrewAI Task configured for solution extraction
    """
    transcript_text = _format_transcripts(transcripts)

    description = f"""Analyse the following engineering team meeting transcripts and extract ALL implementation decisions, planned solutions, and technical choices.

For each solution/decision, identify:
- A unique ID (SOL-001, SOL-002, etc.)
- What is being built or decided
- Any explicit scope limitations (e.g., "12 months" vs a possible "24 months")
- Technologies or tools chosen
- Items explicitly deferred or de-scoped
- Assumptions engineers are making (stated or implied)
- Source transcript filename

Important rules:
- "Let's skip X for now" or "Phase 2" = deferred item
- "Should be fine for the scale" = assumption about scale
- Note when engineers choose LESS than what might be expected (scope limitations)
- Capture technology choices even if briefly mentioned
- If they say "we won't do X" — that's a deliberate scope limitation, not a deferral

TRANSCRIPTS:
{transcript_text}"""

    return Task(
        description=description,
        expected_output=(
            "A structured JSON object with a 'solutions' array containing "
            "all extracted solutions, each with id, statement, scope_limitations, "
            "technologies, deferred, assumptions, and source_transcript fields."
        ),
        agent=agent,
        output_json=SolutionsList,
    )


def create_gap_analysis_task(
    agent: Agent,
    requirements_task: Task,
    solutions_task: Task,
) -> Task:
    """
    The gap analysis task.
    
    Args:
        agent: The gap analysis agent
        requirements_task: Completed requirements extraction task
        solutions_task: Completed solutions extraction task
    
    Returns:
        CrewAI Task configured for gap analysis
    """
    description = """Analyse the requirements (from business team) and solutions (from engineering team) provided in the context from previous tasks.

Cross-reference every requirement against the planned solutions and identify ALL gaps:

1. UNADDRESSED requirements — business needs with NO corresponding engineering solution
2. SCOPE MISMATCHES — engineering partially covers a requirement but with different scope, constraints, or timelines
3. IMPLICIT ASSUMPTIONS — engineering decisions that assume something not validated by business
4. AMBIGUITIES — requirements vague enough that engineering could reasonably misinterpret them

For each gap, provide:
- A unique ID (GAP-001, GAP-002, etc.)
- Type: "unaddressed", "scope_mismatch", "implicit_assumption", or "ambiguity"
- Related requirement IDs
- Related solution IDs (empty list if unaddressed)
- Clear plain-English description
- Severity: "high" (project risk), "medium" (needs clarification), "low" (minor concern)
- A clear, concise and specific question or action to resolve it, do not provide generic answers here.

Rules:
- A requirement is only "addressed" if the solution FULLY covers its scope and constraints
- "We'll do 12 months" when business said "24 months" is a scope_mismatch, not addressed
- "We'll skip SMS" when business said "nice-to-have" is fine — but note it if business emphasis was strong
- Missing GDPR implementation details for an EU deployment is HIGH severity
- Be thorough — every gap is a project risk. Missing a gap is worse than flagging a borderline one.
- Be specific — vague gaps are not actionable
- If related gaps are identified, summarize them into a single gap instead of separate gaps fr each small detail"""

    return Task(
        description=description,
        expected_output=(
            "A structured JSON object with a 'gaps' array containing all "
            "identified gaps, each with gap_id, type, requirement_refs, "
            "solution_refs, description, severity, and suggested_action fields."
        ),
        agent=agent,
        context=[requirements_task, solutions_task],
        output_json=GapReport,
    )


def _format_transcripts(transcripts: List[Dict[str, str]]) -> str:
    """Format transcript list into a readable text block for the prompt."""
    parts = []
    for t in transcripts:
        parts.append(f"--- {t['filename']} ---")
        parts.append(t["content"])
        parts.append("")
    return "\n".join(parts)
