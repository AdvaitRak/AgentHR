# streamlit_app.py

import streamlit as st
from langgraph_app import run_agent

st.set_page_config(page_title="AgentHR", page_icon="🤖")

# Title
st.title("🤖 AgentHR — LLM-Powered HR Assistant")

# Input box
user_input = st.text_input("Ask me anything about your employees 👇", placeholder="e.g., List employees in Pune")

# On button click
if st.button("Ask Agent"):
    if not user_input.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Thinking..."):
            response = run_agent(user_input)

        if response.get("error"):
            st.error(f"❌ Error: {response['error']}")
        elif response.get("query_result"):
            st.success("✅ Here's what I found:")
            st.write(response.get("final_response", "⚠️ No response generated."))

        else:
            st.warning("⚠️ No result returned.")
