"""
Agent definitions for the gap analysis pipeline.

"""
from crewai import Agent, LLM

from .llm_config import get_llm


def create_requirements_agent() -> Agent:
    """
    Create the Requirements Analyst agent.
    
    This agent specializes in reading business meeting transcripts and
    extracting structured requirements with priorities, constraints,
    and traceability back to speakers.
    """
    return Agent(
        role="Senior Requirements Analyst",
        goal=(
            "Extract every business requirement from meeting transcripts, "
            "capturing explicit and implicit needs, priorities, constraints, "
            "and the stakeholder who raised each requirement."
        ),
        backstory=(
            "You are a senior business analyst with 15 years of experience in "
            "enterprise software projects. You've seen countless requirements "
            "fall through the cracks because they were mentioned casually in "
            "meetings but never documented. You have a talent for reading between "
            "the lines — catching implicit requirements that stakeholders assume "
            "are obvious but never explicitly state. You distinguish clearly between "
            "hard requirements (must-haves) and aspirational items (nice-to-haves). "
            "You always trace requirements back to the person who raised them for "
            "accountability."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_solutions_agent() -> Agent:
    """
    Create the Solutions Analyst agent.
    
    This agent specializes in reading engineering meeting transcripts and
    extracting implementation decisions, technology choices, scope limitations,
    and explicitly deferred items.
    """
    return Agent(
        role="Senior Technical Analyst",
        goal=(
            "Extract every implementation decision, technology choice, scope "
            "limitation, and deferred item from engineering meeting transcripts. "
            "Capture what engineers plan to build AND what they explicitly chose "
            "not to build."
        ),
        backstory=(
            "You are a senior solutions architect with deep experience translating "
            "engineering discussions into structured technical documentation. You "
            "understand that what engineers DON'T say is as important as what they "
            "do say. When an engineer says 'let's do 12 months for now', you "
            "recognize that as a scope limitation. When they say 'we'll skip that', "
            "you capture it as a deliberate deferral. You also identify assumptions "
            "engineers are making — the unstated beliefs that drive their decisions "
            "but may not align with business expectations."
        ),
        llm=get_llm(),
        verbose=True,
        allow_delegation=False,
    )


def create_gap_agent() -> Agent:
    """
    Create the Gap Analysis agent.
    
    This agent cross-references requirements against solutions to identify
    gaps, mismatches, risky assumptions, and ambiguities.
    """
    return Agent(
        role="Principal Gap Analyst",
        goal=(
            "Identify every gap between business requirements and engineering "
            "plans — including unaddressed needs, scope mismatches, implicit "
            "assumptions, and ambiguities that could lead to misunderstandings."
        ),
        backstory=(
            "You are a principal project risk analyst who has saved organizations "
            "millions by catching requirement gaps before they reach production. "
            "You think like both a business stakeholder and an engineer, which lets "
            "you spot misalignments others miss. You know that a 'partially addressed' "
            "requirement is often more dangerous than a completely missed one — because "
            "it creates a false sense of coverage. You produce actionable gap reports "
            "with specific questions to resolve each issue, not vague warnings."
        ),
        llm=get_llm(temp=0.2),
        verbose=True,
        allow_delegation=False,
    )
