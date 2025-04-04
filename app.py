import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process
from tasks.hr_tasks import HRTasks
import chromadb  # Make sure chromadb is imported

# Ensure database is stored properly
DB_PATH = "data/chromadb_data"
chroma_client = chromadb.PersistentClient(path=DB_PATH)

# Load environment variables
load_dotenv()

# Streamlit UI
st.title("🛠️ Intelligent Talent Acquisition Assistant")
st.subheader("Automated HR Recruitment System")

# Input field for HR's job-role query
hr_query = st.text_input("Enter Job Role Query:", "")

# Button to start the process
if st.button("Start Recruitment Process"):
    if not hr_query:
        st.warning("Please enter a job role query!")
    else:
        st.write("🔍 Interpreting job role...")

        # Initialize HR tasks
        hr_tasks = HRTasks()

        # Step 1: Interpret HR's query first
        query_crew = Crew(
            agents=[hr_tasks.hr_query_agent()],
            tasks=[hr_tasks.handle_hr_query(hr_query)],
            verbose=True
        )

        # Get the result from CrewOutput object
        crew_output = query_crew.kickoff()
        job_details = str(crew_output)
        job_role = job_details.strip().replace("Job Role:", "").strip()

        st.success(f"Interpreted Job Role: {job_role}")

        # Step 2: Execute tasks
        with st.spinner("Processing recruitment tasks..."):
            hr_crew = Crew(
                agents=[
                    hr_tasks.profile_scraper_agent(job_role),
                    hr_tasks.cv_screening_agent(),
                    hr_tasks.communication_agent(),
                    hr_tasks.interview_scheduler_agent(),
                    hr_tasks.reporting_agent(),
                ],
                tasks=[
                    hr_tasks.scrape_profiles(job_role),
                    hr_tasks.screen_cvs(job_role),
                    hr_tasks.communicate(),
                    hr_tasks.schedule_interviews(),
                    hr_tasks.generate_report()
                ],
                verbose=True,
                process=Process.sequential
            )

            results = hr_crew.kickoff()

        st.success("✅ Recruitment Process Completed!")
        st.text_area("Final Results:", results, height=800)
