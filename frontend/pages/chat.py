import streamlit as st

from frontend.utils.chat import get_openai_model_choices, get_extraction_mechanism_choices, get_unique_pdf_filenames, \
    ask_question, get_file_content_from_backend


def qa_interface():
    st.title("Question Answering Interface")

    # Initialize session state variables
    if 'answer_generated' not in st.session_state:
        st.session_state.answer_generated = False
    if 'user_question' not in st.session_state:
        st.session_state.user_question = ""

    openai_models_choice = st.selectbox("Choose an OpenAI model", get_openai_model_choices())
    extraction_mechanism_choice = st.selectbox("Choose a PDF extraction method", get_extraction_mechanism_choices())
    pdf_file_choice = st.selectbox("Choose a PDF file", get_unique_pdf_filenames())

    st.divider()

    # if pdf_file_choice:
        # pdf_file_obj = get_pdf_object_from_db(pdf_file_choice, extraction_mechanism_choice)

    if all([openai_models_choice, extraction_mechanism_choice, pdf_file_choice]):
        pdf_content = get_file_content_from_backend(pdf_file_choice, openai_models_choice, extraction_mechanism_choice)
        st.subheader("PDF Content Preview")
        st.text_area("PDF Content", pdf_content + "...", height=150, disabled=True)

        st.divider()

        st.subheader(f"Ask a Question")
        user_question = st.text_area(f"Enter a question about your PDF ({pdf_file_choice})", height=100, key="question_input", value=st.session_state.user_question)

        if st.button("Generate Answer"):
            if user_question:
                with st.spinner("Generating answer..."):
                    answer = ask_question(user_question, openai_models_choice, extraction_mechanism_choice, pdf_file_choice)
                    st.subheader("Answer")
                    st.write(answer)
                    st.session_state.answer_generated = True
                    st.session_state.user_question = ""  # Clear the question input

                    st.divider()
            else:
                st.warning("Please enter a question!")

        # Display a new question input if an answer was generated
        if st.session_state.answer_generated:
            st.subheader("Ask Another Question")
            new_question = st.text_area("Enter your next question", height=100, key="new_question_input")
            if st.button("Generate New Answer"):
                if new_question:
                    with st.spinner("Generating answer..."):
                        new_answer = ask_question(new_question, openai_models_choice, extraction_mechanism_choice, pdf_file_choice)
                        st.subheader("New Answer")
                        st.write(new_answer)
                        st.session_state.user_question = new_question  # Store the new question
                else:
                    st.warning("Please enter a new question!")
