import streamlit as st
from streamlit_extras.switch_page_button import switch_page


def document_viewer_page():
    if 'selected_document' in st.session_state and st.session_state.selected_document:
        st.title(f"Viewing {st.session_state.selected_document}")
        # Add your document viewing logic here

        # Add a back button
        if st.button("← Back to documents"):
            switch_page("list_docs")
    else:
        st.warning("No document selected. Please select a document from the main page.")
        if st.button("Return to document list"):
            switch_page("main")
