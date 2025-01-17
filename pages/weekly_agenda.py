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
        agenda_df = pd.DataFrame(agenda)
        agenda_df["Actual Days Worked"] = agenda_df.get("actual_days_worked", 0)

        # Editable DataFrame for Actual Days Worked
        edited_agenda = st.data_editor(
            agenda_df,
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True,
            column_config={
                "days_worked": "Planned Days Worked",
                "Actual Days Worked": st.column_config.NumberColumn(min_value=0, max_value=7, step=1)
            }
        )

        # Update Actual Days Worked in the Database
        for index, row in edited_agenda.iterrows():
            if row["Actual Days Worked"] != agenda_df.loc[index, "actual_days_worked"]:
                update_agenda(
                    row["id"],
                    row["consultant_id"],
                    row["project_id"],
                    row["week"],
                    row["days_worked"],
                    actual_days_worked=row["Actual Days Worked"]
                )
                st.success(f"Updated Actual Days Worked for Week {row['week']}.")

        # Display a button to delete entries
        for _, row in agenda_df.iterrows():
            delete_btn = st.button(f"Delete Schedule for Week {row['week']}", key=f"delete_agenda_{row['id']}")
            if delete_btn:
                delete_agenda(row["id"])
                st.success(f"Schedule for Week {row['week']} deleted successfully!")
                st.experimental_rerun()

    else:
        st.info("No weekly schedules found. Add one using the form above.")

# Call the page function
if __name__ == "__main__":
    weekly_agenda_page()