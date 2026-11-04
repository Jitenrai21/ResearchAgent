from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0)