# import streamlit as st
# from dotenv import load_dotenv

# from frontend.pages.chat import qa_interface
# from frontend.pages.document_viewer import document_viewer_page
# from frontend.pages.list_docs import list_docs_page
# from frontend.pages.user_creation import create_user
# from frontend.pages.user_login import login
# from frontend.pages.summary_generation import summary_generation_page

# def main():
#     # Load environment variables from .env file
#     load_dotenv()

#     # Set page configuration
#     st.set_page_config(
#         page_title="Document Management System",
#         layout="wide",
#         initial_sidebar_state="expanded",
#     )

#     # Custom CSS (unchanged)
#     st.markdown("""
#     <style>
#         .reportview-container {
#             background: linear-gradient(to right, #f3e7e9 0%, #e3eeff 99%, #e3eeff 100%);
#         }
#         .sidebar .sidebar-content {
#             background: linear-gradient(to bottom, #f3e7e9 0%, #e3eeff 99%, #e3eeff 100%);
#         }
#         h1 {
#             color: #1e3d59;
#         }
#         .stButton>button {
#             color: #ffffff;
#             background-color: #1e3d59;
#             border-radius: 5px;
#         }
#         .stTextInput>div>div>input {
#             border-radius: 5px;
#         }
#     </style>
#     """, unsafe_allow_html=True)

#     # Initialize session states
#     if 'current_view' not in st.session_state:
#             st.session_state.current_view = 'document_list'
#     if 'selected_document' not in st.session_state:
#             st.session_state.selected_document = None
#     if 'summaries' not in st.session_state:
#             st.session_state.summaries = {}


#     # if "logged_in" not in st.session_state:
#     #     st.session_state.logged_in = False

#     # def logout():
#     #     if st.button("Logout"):
#     #         st.session_state.logged_in = False
#     #         st.rerun()

#     # # login_page = st.Page(login, title="User Login", icon=":material/login:", default=True)
#     # # logout_page = st.Page(logout, title="Log Out", icon=":material/logout:")
#     # # user_creation_page = st.Page(create_user, title="User Registration")
#     # # qa_page = st.Page(qa_interface, title="Question Answering", icon=":material/chat:")
#     # docs_list = st.Page(list_docs_page, title="Explore Documents", icon="📃")
#     # doc_viewer = st.Page(document_viewer_page, title="Document Viewer")

#     # if st.session_state.logged_in:
#     #     pg = st.navigation({
#     #             "Question Answering Interface": [qa_page],
#     #             "Logout": [logout_page]
#     #         })
#     # else:
#     #     pg = st.navigation({
#     #         "User Login": [login_page],
#     #         "User Creation": [user_creation_page],
#     #     })

#     # pg = st.navigation({
#     #     "Docs List": [docs_list],
#     #     "Document Viewer": [doc_viewer]
#     # })

#     # pg.run()

#     # Sidebar navigation
#     st.sidebar.title("Navigation")
#     nav_selection = st.sidebar.radio(
#             "Go to",
#             ["Document List", "Document Viewer", "Summary Generation"]
#         )

#         # Update current view based on navigation
#     st.session_state.current_view = nav_selection.lower().replace(" ", "_")

#         # Main content area
#     if st.session_state.current_view == "document_list":
#             list_docs_page()
#     elif st.session_state.current_view == "document_viewer":
#             document_viewer_page()
#     elif st.session_state.current_view == "summary_generation":
#             summary_generation_page()

#     if __name__ == "__main__":
#         main()

# File: app.py
import streamlit as st
from dotenv import load_dotenv
import streamlit as st
from dotenv import load_dotenv
from frontend.pages.list_docs import list_docs_page
from frontend.pages.document_viewer import document_viewer_page
from frontend.pages.summary_generation import summary_generation_page
from frontend.pages.chat import qa_interface
def main():
    # Load environment variables
    load_dotenv()

    # Set page configuration
    st.set_page_config(
        page_title="Document Management System",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS
    st.markdown("""
    <style>
        .reportview-container {
            background: linear-gradient(to right, #f3e7e9 0%, #e3eeff 99%, #e3eeff 100%);
        }
        .sidebar .sidebar-content {
            background: linear-gradient(to bottom, #f3e7e9 0%, #e3eeff 99%, #e3eeff 100%);
        }
        h1 {
            color: #1e3d59;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #1e3d59;
            border-radius: 5px;
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
        }
        .summary-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session states
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'document_list'
    if 'selected_document' not in st.session_state:
        st.session_state.selected_document = None
    if 'summaries' not in st.session_state:
        st.session_state.summaries = {}

    # Sidebar navigation
    st.sidebar.title("Navigation")
    nav_selection = st.sidebar.radio(
        "Go to",
        ["Document List", "Document Viewer", "Summary Generation", "Question Answering"]
    )

    # Update current view based on navigation
    st.session_state.current_view = nav_selection.lower().replace(" ", "_")

    # Main content area
    if st.session_state.current_view == "document_list":
        list_docs_page()
    elif st.session_state.current_view == "document_viewer":
        document_viewer_page()
    elif st.session_state.current_view == "summary_generation":
        summary_generation_page()
    elif st.session_state.current_view == "question_answering":
        qa_interface()

if __name__ == "__main__":
    main()
