import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
from backend.config import settings

# Load environment variables from .env file
load_dotenv()

# API base URL
API_BASE_URL = "http://localhost:8000/qa/{article_id}/qa"  # Adjust this to your FastAPI server address

def qa_interface():
    st.title("Question Answering Interface")

    # Initialize session state variables
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_article_id' not in st.session_state:
        st.session_state.current_article_id = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 1  # Replace with actual user authentication

    # Sidebar for article selection
    st.sidebar.title("Research Assistant")
    article_id = st.sidebar.number_input("Enter Article ID", min_value=1, step=1)
    if article_id != st.session_state.current_article_id:
        st.session_state.current_article_id = article_id
        st.session_state.messages = []

    # Main interface
    st.subheader(f"Article #{article_id} Q&A")

    # Get OpenAI model choices
    openai_models_choice = st.selectbox("Choose an OpenAI model", ["gpt-3.5-turbo", "gpt-4"])

    # Get context type choices
    context_type_choice = st.selectbox("Choose context type", ["research", "general", "technical"])

    # Display PDF content preview (you might need to implement this separately)
    if st.session_state.current_article_id:
        st.subheader("PDF Content Preview")
        st.text("PDF content preview not implemented in this version.")

    st.divider()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the article"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the query
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{API_BASE_URL}/chat/{st.session_state.current_article_id}/qa",
                json={
                    "question": prompt,
                    "model": openai_models_choice,
                    "context_type": context_type_choice
                },
                headers={"Authorization": f"Bearer {settings.JWT_SECRET_KEY}"}
            )

            if response.status_code == 200:
                qa_response = response.json()
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                return

        # Display the response
        with st.chat_message("assistant"):
            st.markdown(qa_response["answer"])
            st.markdown(f"**Confidence:** {qa_response['confidence_score']}")
            st.markdown(f"**Referenced Pages:** {', '.join(map(str, qa_response['referenced_pages']))}")
            if qa_response['media_references']:
                st.markdown(f"**Media References:** {', '.join(qa_response['media_references'])}")

        st.session_state.messages.append({"role": "assistant", "content": qa_response["answer"]})

    # Display chat history
    st.sidebar.title("Chat History")
    if st.sidebar.button("Load Chat History"):
        response = requests.get(
            f"{API_BASE_URL}/chat/{st.session_state.current_article_id}/history",
            headers={"Authorization": f"Bearer {settings.JWT_SECRET_KEY}"}
        )

        if response.status_code == 200:
            history = response.json()
            for item in history:
                st.sidebar.markdown(f"**Q:** {item['question']}")
                st.sidebar.markdown(f"**A:** {item['answer']}")
                st.sidebar.markdown(f"**Time:** {item['created_at']}")
                st.sidebar.markdown("---")
        else:
            st.sidebar.error(f"Error loading chat history: {response.status_code} - {response.text}")

if __name__ == "__main__":
    qa_interface()
