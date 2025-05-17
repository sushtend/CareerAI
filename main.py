import streamlit as st
import requests

# -------------------------------
# Config
API_URL = "http://localhost:8000/summarize"  # Replace with your deployed API if needed

# -------------------------------
# State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Ikigai Journaling"
if "journal_submitted" not in st.session_state:
    st.session_state.journal_submitted = False
if "expanded_sections" not in st.session_state:
    st.session_state.expanded_sections = {
        "Introspection": True,
        "Exploration": False,
        "Reflection": False,
        "Action": False
    }
if "action_status" not in st.session_state:
    st.session_state.action_status = {
        "Guided Ikigai journaling": "Not Started",
        "Research Industry/role aligns with your ikigai": "Not Started",
        "Personalised outreach to connect with recruiters/founders": "Not Started"
    }

# -------------------------------
# Login Section
def login():
    st.title("AI Career Launchpad – Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials. Try admin / admin.")

if not st.session_state.logged_in:
    login()
    st.stop()

# -------------------------------
# Sidebar Navigation
st.sidebar.title("Navigation")

menu_structure = {
    "Introspection": [
        ("Ikigai Journaling", True),
        ("Role Research", False),
        ("Recruiter Outreach", False)
    ],
    "Exploration": [
        ("Project Topics", False),
        ("Build-in-Public", False)
    ],
    "Reflection": [
        ("Feedback Funnel", False),
        ("Strength-Weakness", False),
        ("Case Studies", False)
    ],
    "Action": [
        ("Project Tracker", False),
        ("Delta 4", False),
        ("Job Alerts", False)
    ]
}

for phase, sub_items in menu_structure.items():
    with st.sidebar.expander(phase, expanded=st.session_state.expanded_sections[phase]):
        for name, enabled in sub_items:
            if enabled:
                if st.sidebar.button(name, key=name):
                    st.session_state.selected_page = name
            else:
                st.markdown(
                    f"<span style='color:grey;cursor:not-allowed;'>{name}</span>",
                    unsafe_allow_html=True
                )

# -------------------------------
# Main UI
st.title("AI Career Launchpad")

if st.session_state.selected_page == "Ikigai Journaling":
    st.subheader("Phase 1 – Introspection > Ikigai Journaling")

    # -------------------------------
    # Action Item Status – Enhanced View
    st.markdown("### Action Item Status")

    status_colors = {
        "Not Started": "#f0ad4e",
        "In Progress": "#0275d8",
        "Done": "#5cb85c"
    }

    status_icons = {
        "Not Started": "○",
        "In Progress": "⟳",
        "Done": "✔"
    }

    for item, status in st.session_state.action_status.items():
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"<div style='font-size: 16px;'>{item}</div>", unsafe_allow_html=True)
        with col2:
            badge_html = f"""
            <div style='
                background-color: {status_colors[status]};
                padding: 4px 12px;
                border-radius: 15px;
                color: white;
                text-align: center;
                font-size: 13px;
                display: inline-block;
            '>
            {status_icons[status]} {status}
            </div>
            """
            st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------
    # Journaling Form
    st.markdown("## Guided Ikigai Journaling")

    with st.form("journal_form"):
        love = st.text_area("1. What do you love doing?")
        good_at = st.text_area("2. What are you good at?")
        paid_for = st.text_area("3. What can you be paid for?")
        world_needs = st.text_area("4. What does the world need from you?")
        submitted = st.form_submit_button("Submit & Summarize")

    if submitted:
        with st.spinner("Summarizing your Ikigai..."):
            try:
                response = requests.post(API_URL, json={
                    "love": love,
                    "good_at": good_at,
                    "paid_for": paid_for,
                    "world_needs": world_needs
                })
                if response.status_code == 200:
                    result = response.json()
                    st.success("Here’s your AI-generated Ikigai summary:")
                    st.markdown(f"**Summary:** {result['summary']}")
                    st.markdown(f"**Suggested Role:** {result['role']}")
                    st.session_state.journal_submitted = True
                    st.session_state.action_status["Guided Ikigai journaling"] = "Done"
                else:
                    st.error("API error. Please try again.")
            except Exception as e:
                st.error(f"Error calling backend: {e}")

else:
    st.subheader("This section is coming soon.")
    st.info("Only 'Ikigai Journaling' is enabled for now in the MVP.")

# -------------------------------
# Footer
st.markdown("---")
st.caption("This is your personal AI career workspace.")
