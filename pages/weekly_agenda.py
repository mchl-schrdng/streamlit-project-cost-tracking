import streamlit as st
from utils.db_utils import get_consultants, get_projects, add_agenda, get_agenda, update_agenda, delete_agenda

def weekly_agenda_page():
    st.title("Weekly Agenda Management")

    # Add Weekly Schedule Form
    st.subheader("Add Weekly Schedule")
    consultants = get_consultants()
    projects = get_projects()

    if consultants and projects:
        with st.form("add_weekly_schedule_form", clear_on_submit=True):
            consultant = st.selectbox(
                "Select Consultant",
                options=[(c["id"], c["name"]) for c in consultants],
                format_func=lambda x: x[1],
                key="agenda_consultant"
            )
            project = st.selectbox(
                "Select Project",
                options=[(p["id"], p["name"]) for p in projects],
                format_func=lambda x: x[1],
                key="agenda_project"
            )
            week = st.number_input("Week Number", min_value=1, max_value=52, step=1, key="agenda_week")
            days_worked = st.number_input("Days Worked (0-7)", min_value=0, max_value=7, step=1, key="agenda_days")
            submitted = st.form_submit_button("Add Schedule")

            if submitted:
                consultant_id = consultant[0]
                project_id = project[0]
                if days_worked > 0:
                    add_agenda(consultant_id, project_id, week, days_worked)
                    st.success("Weekly schedule added successfully!")
                else:
                    st.error("Days worked must be greater than 0.")
    else:
        st.warning("Please add consultants and projects first.")

    st.divider()

    # Display Weekly Agenda
    st.subheader("All Weekly Schedules")
    agenda = get_agenda()

    if agenda:
        for entry in agenda:
            with st.expander(f"Week {entry['week']}: {entry['consultant_name']} on {entry['project_name']}"):
                # Editable form for each agenda entry
                with st.form(f"edit_agenda_form_{entry['id']}"):
                    consultant = st.selectbox(
                        "Select Consultant",
                        options=[(c["id"], c["name"]) for c in consultants],
                        index=[c["id"] for c in consultants].index(entry["consultant_id"]),
                        format_func=lambda x: x[1],
                        key=f"agenda_edit_consultant_{entry['id']}"
                    )
                    project = st.selectbox(
                        "Select Project",
                        options=[(p["id"], p["name"]) for p in projects],
                        index=[p["id"] for p in projects].index(entry["project_id"]),
                        format_func=lambda x: x[1],
                        key=f"agenda_edit_project_{entry['id']}"
                    )
                    week = st.number_input(
                        "Week Number", 
                        min_value=1, max_value=52, step=1, 
                        value=entry["week"], 
                        key=f"agenda_edit_week_{entry['id']}"
                    )
                    days_worked = st.number_input(
                        "Days Worked (0-7)", 
                        min_value=0, max_value=7, step=1, 
                        value=entry["days_worked"], 
                        key=f"agenda_edit_days_{entry['id']}"
                    )
                    updated = st.form_submit_button("Update")
                    if updated:
                        consultant_id = consultant[0]
                        project_id = project[0]
                        if days_worked > 0:
                            update_agenda(entry["id"], consultant_id, project_id, week, days_worked)
                            st.success("Weekly schedule updated successfully!")
                            st.experimental_rerun()
                        else:
                            st.error("Days worked must be greater than 0.")

                # Delete button
                delete_btn = st.button(f"Delete Schedule for Week {entry['week']}", key=f"delete_agenda_{entry['id']}")
                if delete_btn:
                    delete_agenda(entry["id"])
                    st.success("Schedule deleted successfully!")
                    st.experimental_rerun()
    else:
        st.info("No weekly schedules found. Add one using the form above.")

# Call the page function
if __name__ == "__main__":
    weekly_agenda_page()