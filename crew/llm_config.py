"""LLM configuration for CrewAI agents using Ollama."""
import os

from crewai import LLM

def get_model_name():
    """
    Return the LLM identifier string for CrewAI agents.
    
    Reads configuration from environment variables:
    - OLLAMA_MODEL: Model name (default: llama3.2)

    Returns:
        LLM identifier string.
    """
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")

    return f"ollama/{model}"

def get_llm(temp = 0.1):
    """
    Return LLM objects with set temperature for CrewAI agents.

    Returns:
        CreaAI LLM objects for CrewAI agents.
    """

    model = os.environ.get("OLLAMA_MODEL", "llama3.2")

    return LLM(
        model=f"ollama/{model}",
        temperature=temp
    )



