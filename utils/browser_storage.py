
from pathlib import Path

import streamlit.components.v1 as components


COMPONENT_DIRECTORY = (
    Path(__file__).resolve().parent.parent
    / "browser_storage_component"
)


browser_storage_component = components.declare_component(
    "ai_interview_session_storage",
    path=str(COMPONENT_DIRECTORY),
)


def save_and_restore_session(session_data):
    """
    Save application data in browser session storage
    and return previously saved data when available.
    """

    result = browser_storage_component(
        payload=session_data,
        default=None,
        key="ai_interview_session_storage",
    )

    return result
