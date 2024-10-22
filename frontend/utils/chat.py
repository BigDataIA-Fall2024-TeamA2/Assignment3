import logging
from functools import lru_cache

import streamlit as st

from frontend.utils.auth import make_authenticated_request, make_unauthenticated_request

logger = logging.getLogger(__name__)

@lru_cache
def get_openai_model_choices():
    return make_unauthenticated_request(
        endpoint="/choices/openai-models",
        method="GET"
    )["choices"]


@lru_cache
def get_extraction_mechanism_choices():
    return make_unauthenticated_request(
        endpoint="/choices/pdf-extraction-mechanisms",
        method="GET"
    )["choices"]


@lru_cache
def _get_pdf_files_list():
    return make_authenticated_request(
        endpoint="/choices/pdfs",
        method="GET"
    )


def get_unique_pdf_filenames():
    return set(pdf["filename"] for pdf in _get_pdf_files_list()["docs"])


def get_pdf_object_from_db(pdf_filename: str, extraction_mechanism: str):
    return make_authenticated_request(
        endpoint="/choices/pdf",
        method="GET",
        params={"filename": pdf_filename, "extraction-mechanism": extraction_mechanism}
    )


def set_chat_id(chat_id: str):
    st.session_state.chat_id = chat_id


def get_chat_id():
    if hasattr(st.session_state, "chat_id") and st.session_state.chat_id is not None:
        return st.session_state.chat_id
    logger.error("chat_id not set")


def revoke_chat_id():
    st.session_state.chat_id = None


def initiate_chat(model, extraction_mechanism, filename):
    response = make_authenticated_request(
        endpoint="/chat/initiate",
        method="POST",
        data={
            "openai_model": model,
            "extraction_mechanism": extraction_mechanism,
            "filename": filename
        }
    )
    set_chat_id(response["chat_id"])


def ask_question(question: str, model: str, extraction_mechanism: str, filename: str):
    if get_chat_id() is None:
        initiate_chat(model, extraction_mechanism, filename)

    response = make_authenticated_request(
        endpoint=f"/chat/{get_chat_id()}/qa",
        method="POST",
        data={
            "question": question,
            "model": model,
        }
    )

    return response["llm_response"]


def get_file_content_from_backend(filename: str, model: str, extraction_mechanism: str):
    verify_valid_chat(filename, model, extraction_mechanism)
    return make_authenticated_request(
        endpoint=f"/chat/{get_chat_id()}/file-content",
        method="GET",
    )["file_contents"]


def verify_valid_chat(filename: str, model: str, extraction_mechanism: str):
    if get_chat_id() is None:
        initiate_chat(model, extraction_mechanism, filename)
    else:
        chat_session = make_authenticated_request(
            endpoint=f"/chat/{get_chat_id()}",
            method="GET",
        )
        if filename != chat_session["filename"]:
            initiate_chat(model, extraction_mechanism, filename)
