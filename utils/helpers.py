
import streamlit as st

from utils.browser_storage import save_and_restore_session


PERSISTED_KEYS = [
    "resume_text",
    "resume_analysis",
    "uploaded_resume_name",
    "job_role",
    "interview_type",
    "difficulty",
    "num_questions",
    "interview_questions",
    "current_question_index",
    "user_answers",
    "answer_evaluations",
    "final_report",
    "interview_started",
    "interview_completed",
    "processed_voice_event_ids",
]


def initialize_session_state():
    """Initialize all temporary application data."""

    default_values = {
        "resume_text": None,
        "resume_analysis": None,
        "uploaded_resume_name": None,
        "job_role": None,
        "interview_type": None,
        "difficulty": None,
        "num_questions": 5,
        "interview_questions": [],
        "current_question_index": 0,
        "user_answers": [],
        "answer_evaluations": [],
        "final_report": None,
        "interview_started": False,
        "interview_completed": False,
        "confirm_clear": False,
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_persisted_session_data():
    """Collect application data for browser storage."""

    data = {}

    for key in PERSISTED_KEYS:
        if key in st.session_state:
            value = st.session_state[key]

            if isinstance(value, (set, tuple)):
                value = list(value)

            data[key] = value

    return data


def restore_session_data(saved_data):
    """Restore application data from browser storage."""

    if not isinstance(saved_data, dict):
        return

    for key in PERSISTED_KEYS:
        if key in saved_data:
            st.session_state[key] = saved_data[key]


def recover_browser_session():
    """
    Restore saved data once and send updated data to browser
    storage on every subsequent Streamlit rerun.
    """

    initialized = st.session_state.get(
        "_browser_storage_initialized",
        False,
    )

    # Handle Clear All before normal saving or restoration.
    if st.session_state.get("_browser_storage_clear_requested", False):

        result = save_and_restore_session(
            {"__clear_storage__": True}
        )

        if isinstance(result, dict) and result.get("status") == "cleared":
            st.session_state["_browser_storage_clear_requested"] = False
            st.session_state["_browser_storage_initialized"] = True
            return

        st.stop()

    # IMPORTANT:
    # This call must happen on every rerun so changed data is saved.
    result = save_and_restore_session(
        get_persisted_session_data()
    )

    # Restore saved data only during the first connection.
    if not initialized:

        if not isinstance(result, dict):
            st.stop()

        status = result.get("status")

        if status == "restore":
            restore_session_data(result.get("data", {}))

            st.session_state["_browser_storage_initialized"] = True

            st.rerun()

        elif status == "ready":
            st.session_state["_browser_storage_initialized"] = True

        else:
            st.stop()


def clear_session_state():
    """Clear application data and request browser storage cleanup."""

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    initialize_session_state()

    st.session_state["_browser_storage_initialized"] = False
    st.session_state["_browser_storage_clear_requested"] = True


def apply_custom_styles():
    """Apply the existing application design."""

    st.markdown(
        """
        <style>
        @import url(
          'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
        );

        :root {
            --purple: #5546e8;
            --purple-dark: #4033c8;
            --navy: #17182f;
            --muted: #68748a;
            --background: #f7f8fc;
            --border: #e9eaf2;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        .stApp {
            background: var(--background) !important;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1320px !important;
            padding: 4.5rem 2.5rem 4rem 2.5rem !important;
        }

        [data-testid="stHeader"] {
            background: white !important;
            height: 3.5rem !important;
        }

        [data-testid="stSidebar"] {
            display: none !important;
        }

        h1, .stMarkdown h1 {
            color: var(--navy) !important;
            font-weight: 800 !important;
            letter-spacing: -1.4px !important;
        }

        h2, h3 {
            color: var(--navy) !important;
            font-weight: 700 !important;
        }

        p, li, label {
            color: var(--muted);
        }

        [data-testid="stMarkdownContainer"] p {
            line-height: 1.75;
        }

        .brand-logo {
            background: var(--purple);
            color: white;
            width: 39px;
            height: 39px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 800;
        }

        .brand-name {
            font-size: 21px;
            font-weight: 800;
            color: var(--navy);
            letter-spacing: -0.8px;
            white-space: nowrap;
        }

        [data-testid="stPageLink"] a {
            color: #42465b !important;
            font-weight: 600 !important;
            text-decoration: none !important;
            border-radius: 9px !important;
        }

        [data-testid="stPageLink"] a:hover {
            color: var(--purple) !important;
            background: #f0efff !important;
        }

        .stButton > button,
        .stFormSubmitButton > button {
            min-height: 45px;
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: 0.2s ease;
        }

        .stButton > button[kind="primary"],
        .stFormSubmitButton > button[kind="primary"] {
            background: var(--purple) !important;
            color: white !important;
            border: 1px solid var(--purple) !important;
        }

        .stButton > button[kind="primary"]:hover,
        .stFormSubmitButton > button[kind="primary"]:hover {
            background: var(--purple-dark) !important;
            border-color: var(--purple-dark) !important;
        }

        .stButton > button:not([kind="primary"]) {
            background: white !important;
            color: var(--navy) !important;
            border: 1px solid #dedff0 !important;
        }

        [data-testid="stMetric"] {
            background: white !important;
            border: 1px solid var(--border) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            box-shadow: 0 5px 20px rgba(30, 30, 70, 0.04);
        }

        [data-testid="stMetricLabel"] {
            color: var(--muted) !important;
        }

        [data-testid="stMetricValue"] {
            color: var(--navy) !important;
            font-weight: 800 !important;
        }

        [data-testid="stFileUploader"] {
            background: white !important;
            border: 1px dashed #aaa4e8 !important;
            border-radius: 14px !important;
            padding: 15px !important;
        }

        [data-testid="stTextArea"] textarea,
        [data-testid="stTextInput"] input {
            background: white !important;
            color: var(--navy) !important;
            border: 1px solid #dfe2ec !important;
            border-radius: 10px !important;
        }

        [data-testid="stSelectbox"] > div > div {
            background: white !important;
            border-radius: 10px !important;
        }

        [data-testid="stExpander"] {
            background: white !important;
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
        }

        [data-testid="stAlert"] {
            border-radius: 12px !important;
        }

        [data-testid="stProgressBar"] > div > div {
            background: var(--purple) !important;
        }

        hr {
            border-color: var(--border) !important;
        }

        .section-eyebrow {
            color: var(--purple);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 1.6px;
            text-transform: uppercase;
        }

        .hero-title {
            color: var(--navy);
            font-size: clamp(38px, 5vw, 62px);
            font-weight: 800;
            line-height: 1.12;
            letter-spacing: -2.5px;
        }

        .purple-text {
            color: var(--purple);
        }

        .hero-description {
            color: #68748a;
            font-size: 17px;
            line-height: 1.8;
        }

        .design-card {
            background: white;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 5px 20px rgba(20, 30, 60, 0.035);
        }

        .design-card h3 {
            color: var(--navy);
        }

        .design-card p {
            color: var(--muted);
        }

        .page-banner {
            background: white;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 26px;
            margin-bottom: 24px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Render the shared horizontal navigation bar."""

    initialize_session_state()

    recover_browser_session()

    apply_custom_styles()

    with st.container():

        logo, home, resume, setup, interview, results, clear = st.columns(
            [2.2, 0.8, 1, 0.9, 1.1, 0.9, 0.9],
            vertical_alignment="center",
        )

        with logo:
            st.markdown(
                """
                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                ">
                    <div class="brand-logo">AI</div>
                    <div class="brand-name">InterviewCoach</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with home:
            st.page_link("app.py", label="Home")

        with resume:
            st.page_link(
                "pages/1_Resume_Analysis.py",
                label="Resume",
            )

        with setup:
            st.page_link(
                "pages/2_Interview_Setup.py",
                label="Setup",
            )

        with interview:
            st.page_link(
                "pages/3_Mock_Interview.py",
                label="Interview",
            )

        with results:
            st.page_link(
                "pages/4_Interview_Results.py",
                label="Results",
            )

        with clear:
            if st.button("Clear All", use_container_width=True):
                st.session_state["confirm_clear"] = True

    if st.session_state["confirm_clear"]:

        st.warning(
            "Are you sure you want to clear all interview data?"
        )

        yes, cancel, _ = st.columns([1, 1, 4])

        with yes:
            if st.button("Yes, clear"):
                clear_session_state()
                st.rerun()

        with cancel:
            if st.button("Cancel"):
                st.session_state["confirm_clear"] = False
                st.rerun()

    st.markdown(
        "<hr style='margin-top:18px;margin-bottom:30px;'>",
        unsafe_allow_html=True,
    )
