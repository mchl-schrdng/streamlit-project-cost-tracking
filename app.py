import streamlit as st
from utils.db_utils import init_db, add_consultant, get_consultants, update_consultant, delete_consultant

# Initialize the database
init_db()

# App Title
st.title("Consultants Management")

# Add Consultant Form
st.subheader("Add New Consultant")
with st.form("add_consultant_form", clear_on_submit=True):
    name = st.text_input("Consultant Name", key="name_input")
    role = st.text_input("Role", key="role_input")
    daily_rate = st.number_input("Daily Rate ($)", min_value=0.0, step=0.01, key="rate_input")
    submitted = st.form_submit_button("Add Consultant")
    if submitted:
        if name and role and daily_rate:
            add_consultant(name, role, daily_rate)
            st.success(f"Consultant '{name}' added successfully!")
        else:
            st.error("Please fill out all fields.")

st.divider()

# Display All Consultants
st.subheader("All Consultants")
consultants = get_consultants()

if consultants:
    for consultant in consultants:
        with st.expander(f"{consultant['name']} ({consultant['role']})"):
            # Editable form for each consultant
            with st.form(f"edit_form_{consultant['id']}"):
                new_name = st.text_input("Name", value=consultant['name'], key=f"name_{consultant['id']}")
                new_role = st.text_input("Role", value=consultant['role'], key=f"role_{consultant['id']}")
                new_rate = st.number_input(
                    "Daily Rate ($)", 
                    value=consultant['daily_rate'], 
                    min_value=0.0, 
                    step=0.01, 
                    key=f"rate_{consultant['id']}"
                )
                updated = st.form_submit_button("Update")
                if updated:
                    if new_name and new_role and new_rate:
                        update_consultant(consultant['id'], new_name, new_role, new_rate)
                        st.success(f"Consultant '{new_name}' updated successfully!")
                        st.experimental_rerun()

            # Delete button
            delete_btn = st.button(f"Delete {consultant['name']}", key=f"delete_{consultant['id']}")
            if delete_btn:
                delete_consultant(consultant['id'])
                st.success(f"Consultant '{consultant['name']}' deleted successfully!")
                st.experimental_rerun()
else:
    st.info("No consultants found. Add one using the form above.")