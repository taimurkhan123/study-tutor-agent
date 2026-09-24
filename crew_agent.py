
import os
from crewai import Agent, Task, Crew, LLM
from tools import generate_quiz, search_study_resources

# --- Patch to fix Groq's cache_breakpoint error ---
from litellm_patch import apply_patch
apply_patch()
# --------------------------------------------------

# --- Groq LLM ---
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
        "creating quizzes, and using uploaded study material."
    ),
    backstory=(
        "You are a patient and knowledgeable tutor. You remember what the "
        "student said earlier. When the student uploads a PDF, you read it "
        "carefully and answer based on it. Use your tools when needed."
    ),
    llm=groq_llm,
    tools=[generate_quiz, search_study_resources],
    verbose=True,
    allow_delegation=False,
)


def run_tutor_agent(user_request: str, chat_history=None, pdf_text=None) -> str:
    """
    Run the tutor agent.
    
    Args:
        user_request: The current user message.
        chat_history: List of previous messages (dicts with 'role' and 'content').
        pdf_text: Extracted text from an uploaded PDF (optional).
    """
    context_parts = []

    # --- PDF context ---
    if pdf_text:
        context_parts.append(
            "===== UPLOADED STUDY MATERIAL =====\n"
            f"{pdf_text}\n"
            "===== END OF MATERIAL =====\n"
            "Use the material above when answering. If the user's question "
            "is about the material, answer strictly from it."
        )

    # --- Chat history context ---
    if chat_history:
        recent = chat_history[-6:]  # last 6 messages
        history_text = "\n".join(
            f"{m['role'].capitalize()}: {m['content'][:400]}"
            for m in recent
        )
        context_parts.append(
            "===== PREVIOUS CONVERSATION =====\n"
            f"{history_text}\n"
            "===== END OF HISTORY =====\n"
            "Remember this context. The user may refer to it."
        )

    # --- Current request ---
    context_parts.append(f"CURRENT USER REQUEST:\n{user_request}")

    full_prompt = "\n\n".join(context_parts)

    task = Task(
        description=full_prompt,
        expected_output=(
            "A helpful, accurate, well-structured response that remembers "
            "the conversation and uses the uploaded material when provided."
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
