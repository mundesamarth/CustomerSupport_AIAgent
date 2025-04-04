from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_AI_API_KEY")
base_url = os.getenv("BASE_URL")

## Defining the tools
KNOWLEDGE_BASE = {
    "hours": "Our customer support is available from 9 AM to 6 PM, Monday to Friday.",
    "refund": "Refunds are processed within 5-7 business days after approval.",
    "shipping": "We offer standard and express shipping options. Standard shipping takes 5-7 days, express takes 2-3 days."
}

@tool
def search_knowldege_base(query: str):
    """Searches the basic knowledge base for common customer queries."""
    query_lower = query.lower()  # ✅ FIXED bug here

    for key, value in KNOWLEDGE_BASE.items():
        if key in query_lower:
            return value
    return "I'm sorry, I couldn't find relevant information. Please contact support."

@tool
def contact_support():
    """Provides contact information for customer support"""
    return "You can reach our support team at support@example.com or call us at +44 9876543210."

# Adding tools to our agent and setting up the model
tools = [search_knowldege_base, contact_support]  

# Initializing OpenAI model
model = ChatOpenAI(
    base_url=base_url,
    api_key=api_key,
    model="meta-llama/llama-3.1-70b-instruct:free",
)

# Creating the agent
app = create_react_agent(model, tools)

# Sending message to the agent
print("Hello, I am an AI Agent. Please enter your query below. Type 'exit' or 'quit' to end the conversation.")

while True:
    user_input = input("\nYou: ")  # Getting user input
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting chat.")
        break

    # Sending user input to the agent
    final_state = app.invoke(
        {"messages": [{"role": "user", "content": user_input}]}
    )

    # Extract and print the agent's response
    if "messages" in final_state and final_state["messages"]:  # ✅ FIXED key issue
        print("AI:", final_state["messages"][-1].content)
    else:
        print("AI: I'm sorry, I couldn't find relevant information. Please contact support.")
