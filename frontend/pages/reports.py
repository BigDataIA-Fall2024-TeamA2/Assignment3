import streamlit as st
import requests
from backend.config import settings  # Import settings for JWT token

def generate_research_report_page():
    st.title("Generate Research Report")

    # Form for user input
    with st.form(key='report_form'):
        article_id = st.number_input("Article ID", min_value=1, step=1)
        questions = st.text_area("Questions (one per line)")
        include_media = st.checkbox("Include Media")
        format_type = st.selectbox("Format Type", ["research_notes", "summary", "detailed_analysis"])
        submit_button = st.form_submit_button(label='Generate Report')

    # Function to call the FastAPI endpoint
    def generate_report(article_id, questions, include_media, format_type):
        url = f"http://localhost:8000/qa/{article_id}/generate-report"
        payload = {
            "questions": [q.strip() for q in questions.split('\n') if q.strip()],
            "include_media": include_media,
            "format_type": format_type
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.JWT_SECRET_KEY}"  # Add JWT token for authentication
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    # Handle form submission
    if submit_button:
        if article_id and questions and format_type:
            with st.spinner("Generating report..."):
                try:
                    report = generate_report(article_id, questions, include_media, format_type)
                    st.success("Report generated successfully!")

                    # Display report details
                    st.subheader("Report Details")
                    st.write(f"Report ID: {report['report_id']}")
                    st.write(f"Created At: {report['created_at']}")
                    st.write(f"Validated: {report['validated']}")
                    st.write(f"Indexed: {report['indexed']}")

                    # Display report content
                    st.subheader("Report Content")
                    st.text_area("Content", report['content'], height=300)

                    # Display media references if any
                    if report['media_references']:
                        st.subheader("Media References")
                        for media in report['media_references']:
                            st.write(media)

                    # Option to index the report
                    if st.button("Index Report"):
                        index_url = f"http://localhost:8000/chat/{article_id}/{report['report_id']}/index"
                        headers = {
                            "Authorization": f"Bearer {settings.JWT_SECRET_KEY}"
                        }
                        index_response = requests.post(index_url, headers=headers)
                        if index_response.status_code == 200:
                            st.success("Report indexed successfully!")
                        else:
                            st.error(f"Failed to index report: {index_response.text}")

                except requests.RequestException as e:
                    st.error(f"Error generating report: {str(e)}")
        else:
            st.error("Please fill in all the required fields.")

