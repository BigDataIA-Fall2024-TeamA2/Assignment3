import streamlit as st


def list_documents():
    test_docs = [
        {
            "name": "Document1.pdf",
            "image_uri": "resources/test_images_set/image0.png"
        },
        {
            "name": "Document2.pdf",
            "image_uri": "resources/test_images_set/image0.png"
        },
        {
            "name": "Document3.pdf",
            "image_uri": "resources/test_images_set/image0.png"
        },
        {
            "name": "Document4.pdf",
            "image_uri": "resources/test_images_set/image0.png"
        },
        {
            "name": "Document5.pdf",
            "image_uri": "resources/test_images_set/image0.png"
        }
    ]

    view_option = st.radio("Select Document Exploration Mode", ("Dropdown View", "Grid View"), horizontal=True)

    if view_option == "Dropdown View":
        selected_doc = st.selectbox("Choose a document", [doc["name"] for doc in test_docs])
        if selected_doc:
            st.write(f"You selected the doc: {selected_doc}")
    elif view_option == "Grid View":
        cols = st.columns(5)
        for idx, doc in enumerate(test_docs):
            with cols[idx % 5]:
                st.image(doc["image_uri"], caption=doc["name"], use_column_width=True)
