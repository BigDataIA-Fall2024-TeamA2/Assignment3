import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
from backend.config import settings
import PyPDF2
import io
import base64

# Load environment variables from .env file
load_dotenv()

# API base URL
API_BASE_URL = "http://localhost:8000/qa/{article_id}/qa"  # Adjust this to your FastAPI server address

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def display_pdf(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def qa_interface():
    st.title("Question Answering Interface")

    # Initialize session state variables
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_article_id' not in st.session_state:
        st.session_state.current_article_id = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = 1  # Replace with actual user authentication
    if 'pdf_content' not in st.session_state:
        st.session_state.pdf_content = None

    # File uploader for PDF
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        st.session_state.current_article_id = uploaded_file.name
        st.session_state.pdf_content = uploaded_file.read()
        st.session_state.messages = []  # Clear previous messages

    # Main interface
    if st.session_state.current_article_id:
        st.subheader(f"Article: {st.session_state.current_article_id}")

        # Get OpenAI model choices
        openai_models_choice = st.selectbox("Choose an OpenAI model", ["gpt-3.5-turbo", "gpt-4"])

        # Display PDF content preview
        st.subheader("PDF Content Preview")
        if st.session_state.pdf_content:
            display_pdf(io.BytesIO(st.session_state.pdf_content))

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

            # Process the query (for testing, we'll use a simple response)
            with st.spinner("Thinking..."):
                # In a real scenario, you would send this to your API
                # For now, we'll just return a simple response
                pdf_text = extract_text_from_pdf(io.BytesIO(st.session_state.pdf_content))
                qa_response = {
                    "answer": f"This is a test response for the question: {prompt}\n\nThe PDF content is: {pdf_text[:500]}...",
                    "confidence_score": 0.95,
                    "referenced_pages": [1, 2, 3],
                    "media_references": []
                }

            # Display the response
            with st.chat_message("assistant"):
                st.markdown(qa_response["answer"])
                st.markdown(f"**Confidence:** {qa_response['confidence_score']}")
                st.markdown(f"**Referenced Pages:** {', '.join(map(str, qa_response['referenced_pages']))}")
                if qa_response['media_references']:
                    st.markdown(f"**Media References:** {', '.join(qa_response['media_references'])}")

            st.session_state.messages.append({"role": "assistant", "content": qa_response["answer"]})

    else:
        st.warning("No article selected. Please upload a PDF file before asking questions.")

if __name__ == "__main__":
    qa_interface()
