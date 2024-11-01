# import streamlit as st
# from streamlit_extras.switch_page_button import switch_page


# # def document_viewer_page():
# #     if 'selected_document' in st.session_state and st.session_state.selected_document:
# #         st.title(f"Viewing {st.session_state.selected_document}")
# #         # Add your document viewing logic here

# #         # Add a back button
# #         if st.button("← Back to documents"):
# #             switch_page("list_docs")
# #     else:
# #         st.warning("No document selected. Please select a document from the main page.")
# #         if st.button("Return to document list"):
# #             switch_page("main")

# # Function to display PDF content
# def document_viewer_page():
#     st.title("Document Viewer")
    
#     # Back button to return to document list
#     if st.button("← Back to documents"):
#         switch_page("list_docs")

#     selected_document = st.session_state.get("selected_document")
    
#     if selected_document:
#         st.header(f"Viewing: {selected_document['name']}")
        
#         # Load and display PDF content
#         pdf_path = selected_document["file_path"]
#         with fitz.open(pdf_path) as pdf:
#             num_pages = pdf.page_count
#             st.write(f"Total Pages: {num_pages}")

#             for page_num in range(num_pages):
#                 page = pdf[page_num]
#                 page_text = page.get_text("text")
#                 st.write(f"### Page {page_num + 1}")
#                 st.text(page_text)  # Display page text for now

#                 # To show page as an image (optional)
#                 # pix = page.get_pixmap()
#                 # st.image(pix.tobytes(), caption=f"Page {page_num + 1}")


import streamlit as st
import fitz  # PyMuPDF for handling PDFs
from backend.services.summary_generation import DocumentSummarizer  # Import your summarizer class
from streamlit_extras.switch_page_button import switch_page

# from backend.utilities.document_processors import load_data_from_directory
# from backend.utilities.nvidia_utils import set_environment_variables
from backend.config import settings

def document_viewer_page():
    st.title("Document Viewer")

    if st.session_state.selected_document:
        doc = st.session_state.selected_document
        st.subheader(f"Viewing: {doc['name']}")
        
        try:
            pdf_path = doc["file_path"]
            with fitz.open(pdf_path) as pdf:
                num_pages = pdf.page_count
                st.write(f"Total Pages: {num_pages}")

                for page_num in range(num_pages):
                    page = pdf[page_num]
                    page_text = page.get_text("text")
                    st.write(f"### Page {page_num + 1}")
                    st.text(page_text)

            # Button to generate summary
            if st.button("Generate Summary"):
                summarizer = DocumentSummarizer()
                try:
                    summary = summarizer.summarize_directory(pdf_path, summary_length="medium")
                    st.subheader("Generated Summary")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")

        except Exception as e:
            st.error(f"Error loading PDF: {str(e)}")
    else:
        st.warning("No document selected. Please select a document from the Document List.")

    # Back button to return to document list
    if st.button("← Back to documents"):
        switch_page("list_docs")

# The rest of your Streamlit application setup...