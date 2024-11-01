import streamlit as st
import requests
from typing import Optional


def generate_summary(article_id: int) -> Optional[str]:
    """Generate summary for the given article ID"""
    try:
        response = requests.post(
            f"http://localhost:8000/articles/generate-summary/{article_id}",
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error(f"Article with ID {article_id} not found")
        else:
            st.error("Failed to generate summary. Please try again later.")
        return None
    except Exception as e:
        st.error(f"Error generating summary: {str(e)}")
        return None


def summary_generation_page():
    st.title("Article Summary Generation")

    # Article selection
    article_id = st.number_input("Enter Article ID", min_value=1, step=1)

    # Generate summary button
    if st.button("Generate Summary", key="generate_btn"):
        with st.spinner("Generating summary..."):
            summary_response = generate_summary(article_id)

            if summary_response:
                st.session_state.summaries[article_id] = summary_response
                st.success("Summary generated successfully!")

    # Display existing summaries
    if st.session_state.summaries:
        st.subheader("Generated Summaries")
        for aid, summary_data in st.session_state.summaries.items():
            with st.expander(f"Article {aid}: {summary_data['title']}", expanded=True):
                st.markdown(
                    f"""
                    <div class="summary-container">
                        <h4>Summary</h4>
                        <p>{summary_data['summary']}</p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save Summary", key=f"save_{aid}"):
                        st.info("Save functionality can be implemented here")
                with col2:
                    if st.button("Share Summary", key=f"share_{aid}"):
                        st.info("Share functionality can be implemented here")
