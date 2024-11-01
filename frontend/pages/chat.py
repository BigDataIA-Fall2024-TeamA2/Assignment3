import streamlit as st
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
from backend.config import settings
import PyPDF2
import io
import base64

from dags.data_ingestion.utils import fetch_file_from_s3
from frontend.utils.auth import make_authenticated_request

load_dotenv()


def display_pdf(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def qa_interface():
    st.title("Question Answering Interface")

    # Main interface
    if 'selected_document' in st.session_state and st.session_state.selected_document:
        doc = st.session_state.selected_document
        st.subheader(f"Viewing: {doc['title']}")


        # Get OpenAI model choices
        openai_models_choice = st.selectbox(
            "Choose an OpenAI model", ["gpt-4o", "gpt-4o-mini", "gpt-3.5"]
        )

        # Display PDF content preview
        st.subheader("PDF Content Preview")
        with st.spinner("Loading PDF"):
            pdf_path = fetch_file_from_s3(doc["pdf_url"], None)
            with open(pdf_path, "rb") as f:
                content = f.read()
            display_pdf(io.BytesIO(content))

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
                article_id = doc['a_id']
                data = {
                    "model": openai_models_choice,
                    "question": prompt,
                }
                response = make_authenticated_request(f"/chat/{article_id}/qa", "POST", data)

            # Display the response
            with st.chat_message("assistant"):
                st.markdown(response["response"])

            st.session_state.messages.append(
                {"role": "assistant", "content": response["response"]}
            )

    else:
        st.warning(
            "No article selected. Please upload a PDF file before asking questions."
        )


if __name__ == "__main__":
    st.session_state.messages = []
    qa_interface()
