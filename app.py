import streamlit as st
from utils.db_utils import init_db

# Initialize the database
init_db()

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to:", ["Weekly Agenda", "Consultants", "Projects", "Cost Analysis"])

# Load the appropriate page based on selection
if menu == "Weekly Agenda":
    from pages.weekly_agenda import weekly_agenda_page
    weekly_agenda_page()
elif menu == "Consultants":
    from pages.consultants import consultants_page
    consultants_page()
elif menu == "Projects":
    from pages.projects import projects_page
    projects_page()
elif menu == "Cost Analysis":
    from pages.cost_analysis import cost_analysis_page
    cost_analysis_page()