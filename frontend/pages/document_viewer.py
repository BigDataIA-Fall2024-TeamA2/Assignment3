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
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv  # Load environment variables
from streamlit_extras.switch_page_button import switch_page
from backend.services.summary_generation import DocumentSummarizer  # Ensure this path is correct
import requests
import base64
from frontend.utils.auth import make_unauthenticated_request

# Load environment variables from .env file
load_dotenv()

def fetch_pdf_from_s3(pdf_url):
    """Fetch PDF file from S3 and return the local path."""
    # Retrieve AWS configuration from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")
    bucket_name = os.getenv("AWS_S3_BUCKET")

    # Create an S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    pdf_key = pdf_url  # The path to your PDF file in S3

    try:
        with NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            s3.download_fileobj(bucket_name, pdf_key, tmp_file)
            return tmp_file.name
    except (NoCredentialsError, PartialCredentialsError):
        st.error("AWS credentials not found.")
    except Exception as e:
        st.error(f"Error fetching PDF from S3: {str(e)}")
    return None

def display_pdf(pdf_file):
    base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def document_viewer_page():
    st.title("Document Viewer")

    # Check if a document is selected
    if 'selected_document' in st.session_state and st.session_state.selected_document:
        doc = st.session_state.selected_document
        st.subheader(f"Viewing: {doc['title']}") 
      
 # Display document title
        
        # # Back button to return to document list
        # if st.button("← Back to documents"):
        #     switch_page("list_docs")

        # Fetch the PDF file from S3
        pdf_path = fetch_pdf_from_s3(doc["pdf_url"])
        if pdf_path:
            try:
                with fitz.open(pdf_path) as pdf:
                    num_pages = pdf.page_count
                    st.write(f"Total Pages: {num_pages}")

                    
                    
                    # Display text content for each page
                    for page_num in range(num_pages):
                        page = pdf[page_num]
                        page_text = page.get_text("text")
                        st.write(f"### Page {page_num + 1}")
                        st.text(page_text)
                   
                            # Display PDF content preview
                    # st.subheader("PDF Content Preview")
                    # if st.session_state.pdf_content:
                    #  display_pdf(io.BytesIO(st.session_state.pdf_content))
                
                 # Button to generate summary
                if st.button("Generate Summary"):
                    article_id = doc['a_id']  # Assuming 'id' contains the article ID
                    summary_data = make_unauthenticated_request(f"articles/generate-summary/{article_id}", "POST")
                    # api_url = f"http://your_fastapi_backend/articles/generate-summary/{article_id}"
                    
                    # # Make a POST request to the summary generation endpoint
                    # try:
                    #     response = requests.post(api_url, headers={"Authorization": f"Bearer {token}"})
                    #     response.raise_for_status()  # Raise an error for bad responses
                    #     summary_data = response.json()  # Parse the response JSON
                        
                    #     # Display the generated summary
                    #     st.subheader("Generated Summary")
                    #     st.write(summary_data['summary'])
                    # except requests.exceptions.RequestException as e:
                    #     st.error(f"Error generating summary: {str(e)}")
                
                st.subheader("Generated Summary")
                st.write(summary_data['summary'])
            except Exception as e:
                st.error(f"Error loading PDF: {str(e)}")
    else:
        st.warning("No document selected. Please select a document from the Document List.")
        if st.button("Return to document list"):
            switch_page("main")  # Redirect to main list page 