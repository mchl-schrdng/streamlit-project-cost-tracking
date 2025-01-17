import streamlit as st
import pandas as pd
from utils.db_utils import get_projects, get_agenda, get_consultants

def calculate_costs():
    """
    Calculate budget, prevision, and actual costs for each project.
    Returns a DataFrame with aggregated cost data.
    """
    # Fetch data
    projects = get_projects()
    agenda = get_agenda()
    consultants = {c["id"]: c["daily_rate"] for c in get_consultants()}

    # Prepare data for calculation
    cost_data = []
    for project in projects:
        project_id = project["id"]
        budget = project["budget"]

        # Filter agenda for this project
        project_agenda = [entry for entry in agenda if entry["project_id"] == project_id]

        # Calculate prevision and actual costs
        prevision_cost = sum(entry["days_worked"] * consultants.get(entry["consultant_id"], 0) for entry in project_agenda)
        actual_cost = sum(
            entry.get("actual_days_worked", 0) * consultants.get(entry["consultant_id"], 0) for entry in project_agenda
        )

        cost_data.append({
            "Project": project["name"],
            "Budget": budget,
            "Prevision Cost": prevision_cost,
            "Actual Cost": actual_cost,
            "Variance": budget - actual_cost
        })

    return pd.DataFrame(cost_data)


def cost_analysis_page():
    st.title("Cost Analysis")

    # Calculate costs
    cost_df = calculate_costs()

    if not cost_df.empty:
        # Display editable DataFrame
        st.subheader("Project Cost Summary (Editable)")
        edited_df = st.data_editor(
            cost_df,
            use_container_width=True,
            num_rows="dynamic",
            hide_index=True
        )

        # Update any changes made in the DataFrame
        st.write("Updated Cost Data:")
        st.write(edited_df)

        # Allow exporting to CSV if needed
        csv_data = edited_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cost Summary as CSV",
            data=csv_data,
            file_name="project_cost_summary.csv",
            mime="text/csv"
        )

    else:
        st.warning("No projects or agenda data available. Please ensure projects, consultants, and schedules are added.")

# Call the page function
if __name__ == "__main__":
    cost_analysis_page()
