"""
Streamlit web interface for the chatbot.
This creates a pretty UI so you don't need command line.
"""

import streamlit as st
from agent import ChatbotAgent

# Page configuration
st.set_page_config(
    page_title="🍕 Pizza Bot",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🍕 Pizza Restaurant AI Assistant")
st.write("Ask me anything about our menu, prices, or inventory!")

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This chatbot uses:
    - 🧠 AI (Ollama)
    - 📚 Document Search (FAISS)
    - 🗄️ Live Database (MySQL)
    """)
    
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize session state (keeps data across reloads)
if "agent" not in st.session_state:
    with st.spinner("🚀 Initializing ChatBot..."):
        st.session_state.agent = ChatbotAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("What would you like to know?")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = st.session_state.agent.chat(user_input)
        
        st.write(response)
    
    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.divider()
st.caption("✨ Powered by LangChain + Ollama + FAISS + Streamlit")