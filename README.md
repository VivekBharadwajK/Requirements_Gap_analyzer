# Requirements Gap Agent
Processes business and engineering team transcripts using a CrewAI
multi-agent pipeline to identify gaps between requirements and solutions.
## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                      CrewAI Crew                         │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │ Business        │  │ Engineering     │             │
│  │ Transcripts     │  │ Transcripts     │             │
│  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                       │
│           ▼                    ▼                       │
│  ┌─────────────────┐  ┌─────────────────┐             │
│  │ Requirements    │  │ Solutions       │             │
│  │ Analyst Agent   │  │ Analyst Agent   │             │
│  │ (Task 1)       │  │ (Task 2)       │             │
│  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                       │
│           └───────┬────────────┘                       │
│                   ▼                                    │
│          ┌─────────────────┐                           │
│          │ Gap Analysis    │                           │
│          │ Agent (Task 3)  │                           │
│          └────────┬────────┘                           │
│                   │                                    │
└───────────────────┼────────────────────────────────────┘
                    ▼
           ┌────────────────┐
           │  Gap Report    │
           │ (JSON/Markdown)│
           └────────────────┘
```

### Data Flow

1. **Requirements Analyst Agent** — reads business transcripts, produces structured requirements with priorities, constraints, and traceability.
2. **Solutions Analyst Agent** — reads engineering transcripts, produces structured solutions with scope limitations, tech choices, and deferrals.
3. **Gap Analysis Agent** — consumes both outputs, cross-references them, and produces an actionable gap report.

All three agents run as a **sequential crew** — each task's output feeds into the next via CrewAI's context mechanism.

## Agent Design Decisions

### Structured Output with Pydantic

Each agent produces typed Pydantic models rather than raw strings. This eliminates JSON parsing failures and gives us compile-time guarantees on the data shape flowing between agents.

### Agent Backstories as Prompt Engineering

CrewAI's `backstory` field isn't decorative — it's prompt engineering. By giving each agent a detailed professional background, we get better extraction quality than generic system prompts.

### Sequential Process (Not Hierarchical)

I chose `Process.sequential` over `Process.hierarchical` because:
- The data flow is linear and well-defined
- No runtime decision-making about which agent to invoke next
- Faster execution (no manager agent overhead)

### Temperature Strategy

- Extraction agents use low temperature (0.1) for consistency
- Gap analysis agent uses slightly higher temperature (0.2) for creative gap identification

## Known Limitations

- **Model quality dependency**: Smaller Ollama models may struggle with the structured output requirements. 
- **Context window limits**: Very large transcript sets may exceed model context. 
- **No memory across runs**: Each pipeline run is stateless. Previous gap reports don't inform future analyses.
- **Single-pass extraction**: Requirements mentioned across multiple transcripts aren't merged/deduplicated.

## What I Would Do Next

1. **Add a Reviewer agent** that validates gap report quality and removes false positives
2. **Implement RAG** with a vector store for large transcript archives
3. **Add inter-agent delegation** — let the gap agent ask the requirements agent for clarification
4. **Confidence scoring** per gap entry
5. **Incremental processing** — only re-analyse changed transcripts

## Setup & Run Instructions

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai) installed and running locally
- A model pulled (e.g., `ollama pull llama3.2`)

### Installation

```bash
cd requirements-gap-agent-crewai
pip install -r requirements.txt
```


### Running the Pipeline

```bash
python main.py --business ./transcripts/business --engineering ./transcripts/engineering --output report.json
```

With markdown output:
```bash
python main.py --business ./transcripts/business --engineering ./transcripts/engineering --output report.md --format markdown
```

### Running Tests

```bash
python -m pytest tests/ -v
```
