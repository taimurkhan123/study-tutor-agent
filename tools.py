from crewai.tools import tool
from pypdf import PdfReader


@tool("Extract Text from PDF")
def extract_pdf_text(file_path: str) -> str:
    """Extracts all text from a given PDF file path. Use this when the user
    asks to analyze a PDF document or study material."""
    try:
        reader = PdfReader(file_path)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return text[:8000]
    except Exception as e:
        return f"Error reading PDF: {e}"


@tool("Generate Quiz Questions")
def generate_quiz(topic: str, num_questions: int = 5) -> str:
    """Generates quiz questions for a given study topic. Call this when the
    user asks for practice questions or a quiz."""
    questions = [
        f"1. What is the core principle of {topic}?",
        f"2. Explain the difference between X and Y in {topic}.",
        f"3. Provide a real-world example of {topic}.",
        f"4. What are the common challenges when applying {topic}?",
        f"5. How does {topic} relate to Z?",
    ]
    return "\n".join(questions[:num_questions])


@tool("Search Study Resources")
def search_study_resources(query: str) -> str:
    """Searches for study resources related to a query. Call this when the
    user asks for learning materials, videos, or articles."""
    return (
        f"Found resources for '{query}':\n"
        f"- 'Introduction to {query}' (YouTube tutorial)\n"
        f"- '{query} Explained' (Medium article)\n"
        f"- Official documentation on {query}"
    )
