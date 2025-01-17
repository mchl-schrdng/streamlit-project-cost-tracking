import streamlit as st
from utils.db_utils import init_db

# Initialize the database
init_db()

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Home", "Consultants", "Projects", "Weekly Agenda", "Cost Analysis"])

# Home Section
if menu == "Home":
    st.title("IT Project Cost Tracker")
    st.write("Welcome to the IT Project Cost Tracker!")
    # Add high-level metrics (placeholders for now)
    st.metric("Total Budget", "$0.00")
    st.metric("Total Prevision Cost", "$0.00")
    st.metric("Total Actual Cost", "$0.00")

# Consultants Section
elif menu == "Consultants":
    from pages.consultants import consultants_page
    consultants_page()

# Projects Section
elif menu == "Projects":
    from pages.projects import projects_page
    projects_page()

# Weekly Agenda Section
elif menu == "Weekly Agenda":
    from pages.weekly_agenda import weekly_agenda_page
    weekly_agenda_page()

# Cost Analysis Section
elif menu == "Cost Analysis":
    from pages.cost_analysis import cost_analysis_page
    cost_analysis_page()