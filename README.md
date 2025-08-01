AgentHR: LLM-Powered HR Assistant
AgentHR is an AI-powered HR assistant designed to showcase a robust agentic workflow. This Streamlit web application allows users to interact with a company's employee database using natural language, translating their requests into executable SQL queries and providing concise, data-driven responses.

Key Features
Natural Language Interface: Users can ask questions about employees in plain English, such as "Who works in the AI department?" or "Add a new employee named Jane Doe."

Intelligent SQL Generation: The agent, powered by the Perplexity AI language model, translates user queries into the correct SQL syntax for both SELECT and INSERT operations.

Robust Agentic Workflow: The application uses LangGraph to create a stateful, multi-step workflow that handles decision-making, tool execution, and error handling.

SQLite Database: Data is managed in a lightweight SQLite database, containing a single employees table.

Secure API Key Management: Utilizes Streamlit's secrets.toml for secure handling of API keys during deployment.

Project Structure
llm.py: Initializes and configures the Perplexity AI language model.

langgraph_app.py: Defines the core agent workflow using LangGraph, including nodes for decision-making, tool execution, and final response generation.

sql_tools.py: Contains Python functions to connect to and interact with the hr_agent_demo.sqlite database.

streamlit_app.py: The frontend of the application, built with Streamlit to provide a user-friendly interface.

db/hr_agent_demo.sqlite: The SQLite database file containing employee information.

Getting Started
Follow these steps to set up and run the project locally.

1. Prerequisites
Python 3.9+

A Perplexity API Key

2. Setup
Clone the repository:

git clone <your-repository-url>
cd <your-project-directory>


Create and activate a virtual environment:

python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


(If requirements.txt is not provided, you can generate it with pip freeze > requirements.txt after installing langchain, langgraph, streamlit, and other necessary libraries.)

Configure your API key:
Create a file named .env in the root directory of your project and add your Perplexity API key:

PERPLEXITY_API_KEY="your_api_key_here"


3. Running the Application
To start the web application, run the following command from your terminal:

streamlit run streamlit_app.py


The application will open in your default web browser.
