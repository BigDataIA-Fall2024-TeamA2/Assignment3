# Multi-Modal RAG Application for Document Analysis

## Application Summary

This application is a sophisticated Retrieval-Augmented Generation (RAG) system that allows users to interact with and analyze PDF documents from the CFA Institute Research Foundation Publications. It features a multi-modal approach, combining text and image analysis for comprehensive document exploration.

Links to Resources:
1. [CodeLabs Link]([https://codelabs-preview.appspot.com/?file_id=1WFuc5ShwnSdNSBE-l3amYXxE4B6U5xpitCTYttudxMI#0](https://codelabs-preview.appspot.com/?file_id=17gEwdjYbRR4qBIRmAqFPeYRKOlSqthT9UAZr5AXWEJc#0))
2. [Deployed Streamlit Frontend](http://98.81.209.60:8501/)
3. [Deployed FastAPI Backend](http://98.81.209.60:8000/docs/)
4. [Demo Video](video/video.mov)
  

## Key Features

- **Data Ingestion and Storage**: Automated scraping of CFA Institute publications, including titles, images, summaries, and PDF files.
- **Document Exploration**: User-friendly interface for browsing and selecting documents.
- **On-the-Fly Summary Generation**: Utilizes NVIDIA services for dynamic document summarization.
- **Multi-Modal RAG**: Advanced querying system integrating both text and image data.
- **Q&A Interface**: Interactive system for document-specific queries.
- **Report Generation**: Produces research notes with links to relevant graphs, tables, and pages.

## Frontend (Streamlit)

The frontend provides an intuitive interface with multiple pages:

1. **User Management**: Registration and login functionality.
2. **Document Selection**: Grid view and dropdown list for document browsing.
3. **Summary Generation**: On-demand document summarization.
4. **Q&A Interface**: Interactive querying system for selected documents.
5. **Report Generation**: Creation of detailed research notes.
6. **Search Functionality**: Comprehensive search across documents and research notes.

## Backend (FastAPI)

The backend handles core functionalities:

- **Data Processing**: Integration with Airflow for data scraping and S3 uploads.
- **Database Management**: Snowflake integration for efficient data storage and retrieval.
- **Multi-Modal RAG**: Implements advanced querying capabilities.
- **Authentication**: Secure JWT-based user authentication.
- **API Endpoints**: For document exploration, summary generation, and Q&A interactions.

## Deployment

- Containerized using Docker for easy deployment and scalability.
- Publicly accessible API and Streamlit application.

## Usage Instructions

1. Access the Streamlit frontend via the provided URL.
2. Create an account or log in to an existing one.
3. Explore documents using the grid view or dropdown list.
4. Generate summaries, ask questions, and create research notes for selected documents.
5. Use the search functionality to find specific information across documents and notes.

## Installation
1. Clone the repository
  ```bash
    git clone https://github.com/BigDataIA-Fall2024-TeamA2/Assignment3 && cd Assignment3
  ```
2. Setup local environment by creating a virtual environment and the `.env` file (For *unix systems)
```bash
python3 -m venv venv
./venv/bin/activate.sh
 poetry install
 cp .env.template .env
```
4. Fill in the relevant secrets in `.env` file.
5. The application is dockerized and doesn't depend on external dependencies. Using the following command the frontend, backend applications can be started:
```bash
docker compose up -d



## Resources

- LLAMA Multimodal Report Generation Example
- Multimodal RAG Slide Deck Example
- NVIDIA Multimodal RAG Example

## Attestation

WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK

Contribution:

    a. Gopi Krishna Gorle: 33%
    b. Pranali Chipkar: 33%
    c. Mubin Modi: 33%


```


## Repository Overview
```bash
.
├── README.md
├── airflow.Dockerfile
├── app.py
├── architecture
│   ├── diagrams
│   │   └── assignment3_architecture.png
│   ├── generate_diagrams.py
│   ├── images.png
│   ├── streamlit-logo-primary-colormark-darktext.png
│   └── v1.drawio
├── backend
│   ├── _init_.py
│   ├── config.py
│   ├── data
│   │   └── Lorem_ipsum.pdf
│   ├── database
│   │   ├── _init_.py
│   │   ├── articles.py
│   │   ├── init_db.py
│   │   ├── qa.py
│   │   ├── research_notes.py
│   │   ├── summary.py
│   │   └── users.py
│   ├── logging.conf
│   ├── main.py
│   ├── schemas
│   │   ├── _init_.py
│   │   ├── articles.py
│   │   ├── auth.py
│   │   ├── qa.py
│   │   └── users.py
│   ├── services
│   │   ├── _init_.py
│   │   ├── articles.py
│   │   ├── auth.py
│   │   ├── auth_bearer.py
│   │   ├── qa.py
│   │   ├── rag.py
│   │   ├── summary_generation.py
│   │   └── users.py
│   ├── test.py
│   ├── utilities
│   │   ├── _init_.py
│   │   ├── base_utils.py
│   │   └── nvidia_utils.py
│   └── views
│       ├── _init_.py
│       ├── articles.py
│       ├── auth.py
│       ├── qa.py
│       └── users.py
├── dags
│   ├── _init_.py
│   ├── articles.py
│   ├── data_indexer
│   │   ├── _init_.py
│   │   ├── document_processors.py
│   │   ├── pdf_indexer.py
│   │   └── utils.py
│   ├── data_ingestion
│   │   ├── _init_.py
│   │   ├── scraper.py
│   │   ├── uploader.py
│   │   └── utils.py
│   ├── pipeline.py
│   └── updated_articles_data.json
├── docker-compose.yml
├── frontend
│   ├── _init_.py
│   ├── config.py
│   ├── pages
│   │   ├── _init_.py
│   │   ├── chat.py
│   │   ├── document_viewer.py
│   │   ├── list_docs.py
│   │   ├── reports.py
│   │   ├── summary_generation.py
│   │   ├── user_creation.py
│   │   └── user_login.py
│   └── utils
│       ├── _init_.py
│       ├── api_utils.py
│       ├── auth.py
│       └── chat.py
├── poetry.lock
└── pyproject.toml
