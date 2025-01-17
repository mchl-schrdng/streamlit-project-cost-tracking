import streamlit as st
from utils.db_utils import get_consultants, get_projects, add_agenda, get_agenda, update_agenda

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
            submitted = st.form_submit_button("Assign Consultant")

            if submitted:
                consultant_id = consultant[0]
                project_id = project[0]
                agenda = get_agenda()

                # Assign consultant to all weeks for the project
                for entry in agenda:
                    if entry["project_id"] == project_id:
                        update_agenda(
                            agenda_id=entry["id"],
                            consultant_id=consultant_id,
                        )
                st.success("Consultant assigned to all project weeks!")
                st.rerun()

    st.divider()

    # Display Editable Weekly Agenda
    st.subheader("All Weekly Schedules")
    agenda = get_agenda()

    if agenda:
        # Prepare data for st.data_editor
        data = [
            {
                "Week": entry["week"],
                "Start Date": entry["start_date"],
                "End Date": entry["end_date"],
                "Consultant": entry["consultant_name"] or "Unassigned",
                "Project": entry["project_name"],
                "Planned Days Worked": entry["days_worked"],
                "Actual Days Worked": entry.get("actual_days_worked", 0),
                "Schedule ID": entry["id"],
            }
            for entry in agenda
        ]

        # Editable DataFrame
        edited_data = st.data_editor(
            data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Planned Days Worked": st.column_config.NumberColumn(min_value=0, max_value=7, step=1),
                "Actual Days Worked": st.column_config.NumberColumn(min_value=0, max_value=7, step=1),
            },
            disabled=["Week", "Start Date", "End Date", "Consultant", "Project", "Schedule ID"],  # Lock uneditable columns
        )

        # Update database on changes
        for original, edited in zip(data, edited_data):
            if original["Planned Days Worked"] != edited["Planned Days Worked"]:
                update_agenda(
                    agenda_id=edited["Schedule ID"],
                    days_worked=edited["Planned Days Worked"]
                )
                st.success(f"Updated Planned Days Worked for Week {edited['Week']} ({edited['Start Date']} - {edited['End Date']}).")
                st.rerun()

            if original["Actual Days Worked"] != edited["Actual Days Worked"]:
                update_agenda(
                    agenda_id=edited["Schedule ID"],
                    actual_days_worked=edited["Actual Days Worked"]
                )
                st.success(f"Updated Actual Days Worked for Week {edited['Week']} ({edited['Start Date']} - {edited['End Date']}).")
                st.rerun()

    else:
        st.info("No weekly schedules available.")