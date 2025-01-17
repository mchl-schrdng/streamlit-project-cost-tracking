import streamlit as st
from utils.db_utils import init_db
from pages.weekly_agenda import weekly_agenda_page

# Initialize the database
init_db()

# Title and Header
st.title("Weekly Agenda Management")

# Directly Call Weekly Agenda Page
weekly_agenda_page()