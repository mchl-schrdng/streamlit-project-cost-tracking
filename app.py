import streamlit as st
from utils.db_utils import init_db, add_consultant, get_consultants, update_consultant, delete_consultant

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
    st.title("Consultants Management")
    
    # Add Consultant Form
    with st.form("add_consultant_form"):
        name = st.text_input("Consultant Name")
        role = st.text_input("Role")
        daily_rate = st.number_input("Daily Rate", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Add Consultant")
        if submitted:
            if name and role and daily_rate:
                add_consultant(name, role, daily_rate)
                st.success("Consultant added successfully!")
            else:
                st.error("Please fill out all fields.")
    
    # Display Consultants
    st.write("### All Consultants")
    consultants = get_consultants()
    if consultants:
        for consultant in consultants:
            st.write(f"**{consultant['name']}** ({consultant['role']}) - ${consultant['daily_rate']}/day")
    else:
        st.info("No consultants found.")

# Projects Section (Placeholder)
elif menu == "Projects":
    st.title("Projects Management")
    st.write("Project management functionality coming soon!")

# Weekly Agenda Section (Placeholder)
elif menu == "Weekly Agenda":
    st.title("Weekly Agenda Management")
    st.write("Weekly agenda functionality coming soon!")

# Cost Analysis Section (Placeholder)
elif menu == "Cost Analysis":
    st.title("Cost Analysis")
    st.write("Cost analysis functionality coming soon!")