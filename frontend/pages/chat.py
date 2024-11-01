import streamlit as st
from openai import OpenAI
from backend.services.qa import process_qa_query, get_qa_history
from backend.utilities.document_processors import get_pdf_documents
from datetime import datetime
from dotenv import load_dotenv
import os
from backend.config import settings  # Import the settings

# Load environment variables from .env file
load_dotenv()

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

    # Get OpenAI model choices (you'll need to implement this function)
    openai_models_choice = st.selectbox("Choose an OpenAI model", ["gpt-3.5-turbo", "gpt-4"])

    # Get context type choices (you'll need to implement this function)
    context_type_choice = st.selectbox("Choose context type", ["research", "general", "technical"])

    # Display PDF content preview
    if st.session_state.current_article_id:
        with st.spinner("Loading PDF content..."):
            pdf_content = get_pdf_documents(st.session_state.current_article_id)
        st.subheader("PDF Content Preview")
        st.text_area("PDF Content", pdf_content[:500] + "...", height=150, disabled=True)

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
            openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)  # Use settings here
            response = process_qa_query(
                article_id=st.session_state.current_article_id,
                question=prompt,
                model=openai_models_choice,
                context_type=context_type_choice,
                openai_client=openai_client,
                user_id=st.session_state.user_id
            )

        # Display the response
        with st.chat_message("assistant"):
            st.markdown(response.answer)
            st.markdown(f"**Confidence:** {response.confidence_score}")
            st.markdown(f"**Referenced Pages:** {', '.join(map(str, response.referenced_pages))}")
            if response.media_references:
                st.markdown(f"**Media References:** {', '.join(response.media_references)}")

        st.session_state.messages.append({"role": "assistant", "content": response.answer})

    # Display chat history
    st.sidebar.title("Chat History")
    if st.sidebar.button("Load Chat History"):
        history = get_qa_history(st.session_state.current_article_id, st.session_state.user_id)
        for item in history:
            st.sidebar.markdown(f"**Q:** {item['question']}")
            st.sidebar.markdown(f"**A:** {item['answer']}")
            st.sidebar.markdown(f"**Time:** {item['created_at']}")
            st.sidebar.markdown("---")

if __name__ == "__main__":
    qa_interface()
