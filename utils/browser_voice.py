
from pathlib import Path

import streamlit.components.v1 as components


COMPONENT_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "browser_voice_component"
)


browser_voice_component = components.declare_component(
    "browser_voice_interview",
    path=str(COMPONENT_DIRECTORY),
)


def browser_voice(question, key=None):
    """Display browser voice controls and return submitted transcript."""

    return browser_voice_component(
        question=question,
        default=None,
        key=key,
    )
