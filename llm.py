import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load the .env file containing your GOOGLE_API_KEY
load_dotenv()

# Initialize the Gemini LLM
llm = ChatOpenAI(
    base_url="https://api.perplexity.ai",
    api_key=os.getenv("PERPLEXITY_API_KEY"),
    model="sonar",
    temperature=0.2
)
