from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_AI_API_KEY")
base_url = os.getenv("BASE_URL")

## Defining out the tools

KNOWLEDGE_BASE = {
    "hours":"Our customer support is available from 9 AM to 6 PM, Monday to Friday",
    "refund":"Refunds are processed within 5-7 business days after approval",
    "shipping":"We offer standard and express shipping options. standard shipping take 5-7 days, express takes 2-3 days."
}

@tool
def search_knowldege_base(query:str):
    """Searches the basic knowledge base for common customer quereis."""
    for key, value in KNOWLEDGE_BASE.items():
        if key in query.lower():
            return value
    return "I'm sorry, I could't find relevant information, Please contact support."

@tool
def contact_support():
    """Provides contact information for customer support"""
    return "You can reach our suport team at support@example.com or call us at +44 9876543210."

# Adding tools to out agent, and setting up the model

tools = [search_knowldege_base, contact_support]  # list of the available tools defined

# Initialising OpenAI model
model = ChatOpenAI(
    base_url = base_url,
    api_key = api_key,
    model = "meta-llama/llama-3.1-70b-instruction:free",
)

#Creating the agent
app = create_react_agent(model,tools)



