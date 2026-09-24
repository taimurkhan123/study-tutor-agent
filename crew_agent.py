
import os
from crewai import Agent, Task, Crew, LLM
from tools import extract_pdf_text, generate_quiz, search_study_resources

# --- Apply the patch BEFORE creating the LLM ---
from litellm_patch import apply_patch
apply_patch()
# ------------------------------------------------

# --- Groq + GPT-OSS-120B ---
groq_llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
)

# --- Single Agent ---
tutor_agent = Agent(
    role="Expert Study Tutor",
    goal=(
        "Help students learn by explaining concepts, answering questions, "
        "creating quizzes, and finding study resources."
    ),
    backstory=(
        "You are a patient and knowledgeable tutor. You break down complex "
        "topics into simple parts. Use your tools when needed to provide "
        "accurate information and create helpful study aids."
    ),
    llm=groq_llm,
    tools=[extract_pdf_text, generate_quiz, search_study_resources],
    verbose=True,
    allow_delegation=False,
)

def run_tutor_agent(user_request: str) -> str:
    task = Task(
        description=user_request,
        expected_output=(
            "A helpful, accurate, and well-structured response that "
            "fulfills the user's study request."
        ),
        agent=tutor_agent,
    )
    crew = Crew(
        agents=[tutor_agent],
        tasks=[task],
        verbose=True,
    )
    result = crew.kickoff()
    return str(result)
