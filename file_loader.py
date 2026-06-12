"""
Transcript file loader — shared utility for loading transcript files from disk.
Separated from main.py to allow testing without CrewAI dependencies.
"""
import sys
from pathlib import Path
from typing import List, Dict


def load_transcripts(directory: str) -> List[Dict[str, str]]:
    """
    Load all transcript files from a directory.

    Handles .txt and .md files. Skips empty files gracefully.

    Args:
        directory: Path to directory containing transcript files

    Returns:
        List of dicts with 'filename' and 'content' keys
    """
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        sys.exit(1)

    transcripts = []
    extensions = {".txt", ".md"}

    for filepath in sorted(dir_path.iterdir()):
        if filepath.suffix.lower() in extensions and filepath.is_file():
            try:
                content = filepath.read_text(encoding="utf-8")
                if content.strip():
                    transcripts.append({
                        "filename": filepath.name,
                        "content": content,
                    })
                else:
                    print(f"Warning: Skipping empty file '{filepath.name}'")
            except (IOError, UnicodeDecodeError) as e:
                print(f"Warning: Could not read '{filepath.name}': {e}")

    if not transcripts:
        print(f"Warning: No valid transcript files found in '{directory}'")

    return transcripts
