
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda, RunnableConfig
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from llm import llm
from tools.sql_tools import query_db, update_db
import json
from typing import TypedDict, Optional, Union



class AgentState(TypedDict, total=False):
    input: str                         
    tool_call: Optional[str]           
    tool_name: Optional[str]           
    tool_input: Optional[str]         
    query_result: Optional[Union[str, list]]  
    final_response: Optional[str]
    error: Optional[str]


@tool
def query_tool(sql: str) -> str:
    """Run SELECT queries on the HR database."""
    result = query_db(sql)
    return str(result)

@tool
def update_tool(sql: str) -> str:
    """Run INSERT/UPDATE/DELETE queries on the HR database."""
    result = update_db(sql)
    return str(result)


def llm_decide_tool(state: AgentState) -> AgentState:
    user_input = state.get("input", "")


    prompt = f"""
You are an internal HR SQL expert working on a SQLite database.

The table `employees` has:
- id
- name
- role
- department
- location
- doj (date of joining)

The official department names in the database are: 'AI', 'Backend', 'HR', 'Product','Infrastructure',
When a user asks about a department, map their request to one of these official names.
For example, 'data science', 'ML', or 'artificial intelligence' should be mapped to the 'AI' department.
'Human Resources' should be mapped to 'HR'.

To calculate years of work, use:
  (julianday('now') - julianday(doj)) / 365.25

Never use DATEDIFF(). It's not valid in SQLite.

Return a JSON object like:
{{
  "tool_name": "query_tool",
  "tool_input": "SELECT name FROM employees;"
}}
OR
{{
  "tool_name": "update_tool",
  "tool_input": "INSERT INTO employees (name, role, department, location, doj) VALUES ('John Doe', 'Data Analyst', 'Analytics', 'Pune', '2023-01-18');"
}}

User query: "{user_input}"
    """

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        print("🔍 LLM RAW:", response.content)

        parsed = json.loads(response.content)

        return {
            **state,
            "tool_call": response.content,
            "tool_name": parsed["tool_name"],
            "tool_input": parsed["tool_input"],
        }

    except Exception as e:
        return {
            **state,
            "error": f"LLM error: {e}"
        }


def execute_tool(state: AgentState) -> AgentState:
    import json

    tool_info = json.loads(state["tool_call"])
    tool_name = tool_info["tool_name"]
    tool_input = tool_info["tool_input"]

    if tool_name == "query_tool":
        result = query_tool.invoke(tool_input)
    elif tool_name == "update_tool":
        result = update_tool.invoke(tool_input)
    else:
        result = f"Unknown tool: {tool_name}"

    return {
        **state,  
        "query_result": result  
    }


def final_response(state: AgentState) -> AgentState:
    result = state.get("query_result") or state.get("output") or " No result available."
    user_input = state.get("input", "")

    prompt = f"""
You are an internal HR assistant for a company.

Only answer questions based on the data from the SQL query output below. 
Do NOT guess, and do NOT use any public or general internet information.

User asked: "{user_input}"

SQL result: {result}

Using only this information, write a friendly and clear answer.
If the result is empty or not helpful, say so.
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        **state,
        "final_response": response.content
    }




def build_graph():
        graph = StateGraph(AgentState)

        graph.add_node("decide_tool", RunnableLambda(llm_decide_tool))
        graph.add_node("execute_sql", RunnableLambda(execute_tool))
        graph.add_node("respond", RunnableLambda(final_response))

        graph.set_entry_point("decide_tool")

        
        def route_tool_call(state):
            if state.get("tool_call"):
                return "execute_sql"
            else:
                return "respond"  
                
        graph.add_conditional_edges(
            "decide_tool",
            route_tool_call
        )

        graph.add_edge("execute_sql", "respond")
        graph.set_finish_point("respond")

        return graph.compile()


def run_agent(user_input: str):
    workflow = build_graph()
    result = workflow.invoke({"input": user_input})
    print("FINAL STATE:", result)
    return result
