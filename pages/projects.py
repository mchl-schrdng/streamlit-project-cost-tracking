import streamlit as st
from utils.db_utils import add_project, get_projects, update_project, delete_project

def projects_page():
    st.title("Projects Management")

    # Add Project Form
    st.subheader("Add New Project")
    with st.form("add_project_form", clear_on_submit=True):
        name = st.text_input("Project Name", key="project_name_input")
        description = st.text_area("Description (optional)", key="project_desc_input")
        budget = st.number_input("Budget ($)", min_value=0.0, step=0.01, key="project_budget_input")
        start_date = st.date_input("Start Date", key="project_start_input")
        end_date = st.date_input("End Date", key="project_end_input")
        submitted = st.form_submit_button("Add Project")
        if submitted:
            if name and budget and start_date and end_date:
                if start_date > end_date:
                    st.error("Start Date cannot be after End Date.")
                else:
                    add_project(name, description, budget, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
                    st.success(f"Project '{name}' added successfully!")
            else:
                st.error("Please fill out all required fields.")

    st.divider()

    # Display All Projects
    st.subheader("All Projects")
    projects = get_projects()

    if projects:
        for project in projects:
            with st.expander(f"{project['name']}"):
                # Editable form for each project
                with st.form(f"edit_form_{project['id']}"):
                    new_name = st.text_input("Name", value=project['name'], key=f"project_name_{project['id']}")
                    new_description = st.text_area(
                        "Description (optional)", 
                        value=project['description'], 
                        key=f"project_desc_{project['id']}"
                    )
                    new_budget = st.number_input(
                        "Budget ($)", 
                        value=project['budget'], 
                        min_value=0.0, 
                        step=0.01, 
                        key=f"project_budget_{project['id']}"
                    )
                    new_start_date = st.date_input(
                        "Start Date", 
                        value=project['start_date'], 
                        key=f"project_start_{project['id']}"
                    )
                    new_end_date = st.date_input(
                        "End Date", 
                        value=project['end_date'], 
                        key=f"project_end_{project['id']}"
                    )
                    updated = st.form_submit_button("Update")
                    if updated:
                        if new_start_date > new_end_date:
                            st.error("Start Date cannot be after End Date.")
                        else:
                            update_project(
                                project['id'], 
                                new_name, 
                                new_description, 
                                new_budget, 
                                new_start_date.strftime('%Y-%m-%d'), 
                                new_end_date.strftime('%Y-%m-%d')
                            )
                            st.success(f"Project '{new_name}' updated successfully!")
                            st.experimental_rerun()

                # Delete button
                delete_btn = st.button(f"Delete {project['name']}", key=f"delete_{project['id']}")
                if delete_btn:
                    delete_project(project['id'])
                    st.success(f"Project '{project['name']}' deleted successfully!")
                    st.experimental_rerun()
    else:
        st.info("No projects found. Add one using the form above.")