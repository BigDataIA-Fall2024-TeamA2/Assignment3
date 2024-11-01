import streamlit as st
from PIL import Image
import io
import base64


def _get_image_base64(image_path):
    """Convert image to base64 string"""
    with Image.open(image_path) as img:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()


def list_docs_page():
    st.title("Document List")

    test_docs = [
        {
            "name": "Sample_Document1.pdf",
            "file_path": "resources/documents/sample_document2.pdf",
            "image_uri": "resources/test_images_set/sample_image.jpg",
        },
        {
            "name": "Sample_Document2.pdf",
            "file_path": "resources/documents/sample_document2.pdf",
            "image_uri": "resources/test_images_set/sample_image.jpg",
        },
        {
            "name": "Sample_Document3.pdf",
            "file_path": "resources/documents/sample_document2.pdf",
            "image_uri": "resources/test_images_set/sample_image.jpg",
        },
    ]

    view_option = st.radio(
        "Select Document Exploration Mode",
        ("Dropdown View", "Grid View"),
        horizontal=True,
    )

    if view_option == "Dropdown View":
        selected_doc_name = st.selectbox(
            "Choose a document", [doc["name"] for doc in test_docs]
        )
        if selected_doc_name:
            if st.button(f"View {selected_doc_name}"):
                selected_doc = next(
                    (doc for doc in test_docs if doc["name"] == selected_doc_name), None
                )
                if selected_doc:
                    st.session_state.selected_document = selected_doc
                    st.session_state.current_view = "document_viewer"
                    st.rerun()

    elif view_option == "Grid View":
        cols = st.columns(3)
        for idx, doc in enumerate(test_docs):
            with cols[idx % 3]:
                img_base64 = _get_image_base64(doc["image_uri"])
                st.image(f"data:image/png;base64,{img_base64}", use_column_width=True)
                st.write(doc["name"])
                if st.button(f"View {doc['name']}", key=f"view_{idx}"):
                    st.session_state.selected_document = doc
                    st.session_state.current_view = "document_viewer"
                    st.rerun()
