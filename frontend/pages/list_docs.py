import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import base64
from PIL import Image
import io


def _get_image_base64(image_path):
    """Convert image to base64 string"""
    with Image.open(image_path) as img:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()


def list_docs_page():
    test_docs = [
        {
            "name": "Document1.pdf",
            "image_uri": "resources/test_images_set/image0.png",
            "target_page": "document_viewer"
        },
        {
            "name": "Document2.pdf",
            "image_uri": "resources/test_images_set/image0.png",
            "target_page": "document_viewer"
        },
        {
            "name": "Document3.pdf",
            "image_uri": "resources/test_images_set/image0.png",
            "target_page": "document_viewer"
        },
        {
            "name": "Document4.pdf",
            "image_uri": "resources/test_images_set/image0.png",
            "target_page": "document_viewer"
        },
        {
            "name": "Document5.pdf",
            "image_uri": "resources/test_images_set/image0.png",
            "target_page": "document_viewer"
        },
    ]

    # Initialize session state if not exists
    if 'selected_document' not in st.session_state:
        st.session_state.selected_document = None

    # Add CSS for hover effect and styling
    st.markdown("""
        <style>
        .image-link {
            display: block;
            position: relative;
            margin: 5px;
            cursor: pointer;
        }
        .image-link:hover {
            transform: scale(1.02);
            transition: transform 0.2s;
        }
        .image-caption {
            text-align: center;
            margin-top: 5px;
            color: #666;
            font-size: 0.9em;
        }
        </style>
    """, unsafe_allow_html=True)

    view_option = st.radio("Select Document Exploration Mode", ("Dropdown View", "Grid View"), horizontal=True)

    if view_option == "Dropdown View":
        selected_doc = st.selectbox("Choose a document", [doc["name"] for doc in test_docs])
        if selected_doc:
            if st.button(f"View {selected_doc}"):
                st.session_state.selected_document = selected_doc
                target_page = next(doc["target_page"] for doc in test_docs if doc["name"] == selected_doc)
                switch_page(target_page)

    elif view_option == "Grid View":
        cols = st.columns(5)
        for idx, doc in enumerate(test_docs):
            with cols[idx % 5]:
                # Convert image to base64
                img_base64 = _get_image_base64(doc["image_uri"])

                # Create clickable image with HTML
                html = f"""
                    <div class="image-link" onclick="window.location.href='/{doc['target_page']}'" 
                         onmouseover="this.style.opacity='0.8'" 
                         onmouseout="this.style.opacity='1'">
                        <img src="data:image/png;base64,{img_base64}" 
                             style="width: 100%; height: auto; border-radius: 10px;">
                        <div class="image-caption">{doc['name']}</div>
                    </div>
                """
                st.markdown(html, unsafe_allow_html=True)

                # Store document info in session state when clicked
                # Note: This requires JavaScript injection which Streamlit doesn't support directly
                # So we'll use a workaround with query parameters
                current_url = st.query_params
                if current_url.get('document') == [doc['name']]:
                    st.session_state.selected_document = doc['name']
                    switch_page(doc['target_page'])
