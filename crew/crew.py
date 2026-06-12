"""
assembles agents and tasks into a runnable pipeline.

"""
from typing import List, Dict, Any, Tuple

from crewai import Crew, Process

from .agents import (
    create_requirements_agent,
    create_solutions_agent,
    create_gap_agent,
)
from .tasks import (
    create_requirements_task,
    create_solutions_task,
    create_gap_analysis_task,
)
from models import RequirementsList, SolutionsList, GapReport


def run_gap_analysis_crew(
    business_transcripts: List[Dict[str, str]],
    engineering_transcripts: List[Dict[str, str]],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Run the full gap analysis crew pipeline.
    
    Creates three agents, assigns them tasks in sequence, and executes
    the crew. Returns structured outputs from all three stages.
    
    Args:
        business_transcripts: List of dicts with 'filename' and 'content'
        engineering_transcripts: List of dicts with 'filename' and 'content'
    
    Returns:
        Tuple of (requirements_list, solutions_list, gaps_list)
        Each is a list of dictionaries matching the Pydantic model schemas.
    """
    # Create agents
    requirements_agent = create_requirements_agent()
    solutions_agent = create_solutions_agent()
    gap_agent = create_gap_agent()

    # Create tasks
    requirements_task = create_requirements_task(
        agent=requirements_agent,
        transcripts=business_transcripts,
    )
    solutions_task = create_solutions_task(
        agent=solutions_agent,
        transcripts=engineering_transcripts,
    )
    gap_task = create_gap_analysis_task(
        agent=gap_agent,
        requirements_task=requirements_task,
        solutions_task=solutions_task,
    )

    # Assemble the crew
    crew = Crew(
        agents=[requirements_agent, solutions_agent, gap_agent],
        tasks=[requirements_task, solutions_task, gap_task],
        process=Process.sequential,
        verbose=True,
    )

    # Execute the pipeline
    result = crew.kickoff()

    # Extract structured outputs from task results
    requirements = _extract_task_output(requirements_task, "requirements")
    solutions = _extract_task_output(solutions_task, "solutions")
    gaps = _extract_task_output(gap_task, "gaps")

    return requirements, solutions, gaps


def _extract_task_output(task, key: str) -> List[Dict[str, Any]]:
    """
    Extract the list output from a CrewAI task.
    
    Handles both Pydantic model outputs and raw dict outputs
    that CrewAI may return depending on model compliance.
    """
    try:
        # Try accessing the pydantic output
        if hasattr(task, "output") and task.output is not None:
            output = task.output
            
            # If it's a CrewOutput or TaskOutput with pydantic
            if hasattr(output, "pydantic") and output.pydantic is not None:
                model = output.pydantic
                if hasattr(model, key):
                    items = getattr(model, key)
                    return [item.model_dump() for item in items]
            
            # If it's a dict (json_dict output)
            if hasattr(output, "json_dict") and output.json_dict is not None:
                data = output.json_dict
                if isinstance(data, dict) and key in data:
                    return data[key]
                elif isinstance(data, list):
                    return data
            
            # Try raw string parsing as fallback
            if hasattr(output, "raw") and output.raw:
                import json
                try:
                    data = json.loads(output.raw)
                    if isinstance(data, dict) and key in data:
                        return data[key]
                    elif isinstance(data, list):
                        return data
                except (json.JSONDecodeError, TypeError):
                    pass

    except Exception as e:
        print(f"Warning: Could not extract '{key}' from task output: {e}")

    return []
