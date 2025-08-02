"""Builds and formats the system prompt for the robot action planner using environment and action JSON data."""

from pathlib import Path
import json
import logging


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / "data"

PROMPT_PATH = DATA_DIR / "prompt.txt"
ENV_PATH = DATA_DIR / "environment.json"
ACTIONS_PATH = DATA_DIR / "actions.json"


def build_system_prompt() -> str:
    """
    Build the system prompt by loading and formatting the environment,
    actions, and the prompt template file.

    :return: The formatted system prompt string.
    """
    environment = load_and_format_environment(ENV_PATH)
    actions = load_and_format_actions(ACTIONS_PATH)
    prompt_template = load_text(PROMPT_PATH)
    try:
        prompt = prompt_template.format(ENVIRONMENT=environment, ACTIONS=actions)
    except KeyError as e:
        raise RuntimeError(f"Missing placeholder in prompt template: {e}")
    logging.info(f"Loaded system prompt:\n{prompt}")
    return prompt


def load_and_format_environment(path: Path) -> str:
    """
    Load the environment JSON file and format it into a string description.

    :param path: Path to the environment JSON file.
    :return: The formatted environment description string.
    """
    try:
        with path.open() as f:
            env = json.load(f)
        return format_environment(env)
    except Exception as e:
        raise RuntimeError(f"Failed to load or format environment: {e}")


def load_and_format_actions(path: Path) -> str:
    """
    Load the actions JSON file and format it into a string description.

    :param path: Path to the actions JSON file.
    :return: The formatted actions description string.
    """
    try:
        with path.open() as f:
            actions = json.load(f)
        return format_actions(actions)
    except Exception as e:
        raise RuntimeError(f"Failed to load or format actions: {e}")


def load_text(path: Path) -> str:
    """
    Load and return the contents of a text file.

    :param path: Path to the text file.
    :return: The file contents as a string.
    """
    try:
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        return prompt
    except Exception as e:
        raise RuntimeError(f"Failed to load prompt template: {e}")


def format_environment(env: dict) -> str:
    """
    Format the environment dictionary into a readable string.

    :param env: The robot environment data loaded from JSON.
    :return: The formatted environment string.
    """
    return "; ".join(
        f"{obj['color']} {obj['type']} (id: {obj['id']}) at position {obj['position']}"
        for obj in env.get("objects", [])
    )


def format_actions(actions: list[dict]) -> str:
    """
    Format the possible robot actions list into a readable string.

    :param actions: List of action definitions loaded from JSON.
    :return: The formatted actions string.
    """
    return "; ".join(f"{a['name']}({', '.join(a['parameters'])})" for a in actions)
