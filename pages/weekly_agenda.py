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
            days_worked = st.number_input("Planned Days Worked (0-7)", min_value=0, max_value=7, step=1, key="agenda_days")
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

    # Display Weekly Agenda with Actual Days Worked
    st.subheader("All Weekly Schedules")
    agenda = get_agenda()

    if agenda:
        # Prepare data for Streamlit's st.data_editor
        data = [
            {
                "Week": entry["week"],
                "Consultant": entry["consultant_name"],
                "Project": entry["project_name"],
                "Planned Days Worked": entry["days_worked"],
                "Actual Days Worked": entry.get("actual_days_worked", 0),
                "Schedule ID": entry["id"],
            }
            for entry in agenda
        ]

        # Use st.data_editor to display and edit the data
        edited_data = st.data_editor(
            data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Planned Days Worked": "number",
                "Actual Days Worked": st.column_config.NumberColumn(min_value=0, max_value=7, step=1),
            },
            disabled=["Week", "Consultant", "Project", "Schedule ID"],  # Prevent editing non-editable fields
        )

        # Check for changes and update the database
        for original, edited in zip(data, edited_data):
            if original["Actual Days Worked"] != edited["Actual Days Worked"]:
                update_agenda(
                    edited["Schedule ID"],
                    actual_days_worked=edited["Actual Days Worked"],
                )
                st.success(f"Updated Actual Days Worked for Week {edited['Week']}.")

        # Display delete buttons
        for entry in data:
            delete_btn = st.button(f"Delete Schedule for Week {entry['Week']}", key=f"delete_agenda_{entry['Schedule ID']}")
            if delete_btn:
                delete_agenda(entry["Schedule ID"])
                st.success(f"Schedule for Week {entry['Week']} deleted successfully!")
                st.experimental_rerun()
    else:
        st.info("No weekly schedules found. Add one using the form above.")

# Call the page function
if __name__ == "__main__":
    weekly_agenda_page()