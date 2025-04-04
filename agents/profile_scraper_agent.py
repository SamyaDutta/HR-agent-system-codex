from crewai import Agent
from langchain_mistralai.chat_models import ChatMistralAI
import os

class ProfileScraperAgent:
    @staticmethod
    def agent(job_role=None):  # Add job_role parameter with default value
        llm = ChatMistralAI(
            api_key=os.getenv("MISTRAL_API_KEY"),
            model="mistral/mistral-large-latest"
        )
        
        # Use the job_role in the agent definition
        return Agent(
            role="Profile Scraper",
            goal=f"Find profiles matching the '{job_role}' job role",
            backstory="Expert in finding and collecting candidate profiles for technical positions.",
            llm=llm,
            allow_delegation=False
        )