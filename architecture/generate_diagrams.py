from diagrams import Cluster, Diagram
from diagrams.generic.storage import Storage
from diagrams.programming.language import Python
from diagrams.aws.storage import S3
from diagrams.saas.analytics import Snowflake
from diagrams.custom import Custom
from diagrams.onprem.workflow import Airflow
from diagrams.programming.framework import Fastapi
from diagrams.programming.flowchart import Action


# Define custom icons for Streamlit and NVIDIA services
class StreamlitIcon(Custom):
    def __init__(self, label):
        super().__init__(
            label=label,
            icon_path="/Users/pranalichipkar/Documents/Pranali/BigData-Assignments/Assignment3/architecture/streamlit-logo-primary-colormark-darktext.png",
        )


class NvidiaIcon(Custom):
    def __init__(self, label):
        super().__init__(
            label=label,
            icon_path="/Users/pranalichipkar/Documents/Pranali/BigData-Assignments/Assignment3/architecture/images.png",
        )


def generate_assignment3_architecture():
    with Diagram(
        "Assignment 3 Architecture",
        direction="LR",
        filename="diagrams/assignment3_architecture",
        outformat="png",
        show=False,
    ) as dia:

        # Part 1: Data Ingestion and Database Population - Entirely Airflow Managed
        with Cluster("Data Ingestion and Storage"):
            airflow = Airflow("Airflow Pipeline")  # Airflow managing the pipeline

            # Airflow-managed flow for data source, scraping, and storage
            with Cluster("Airflow Managed Flow"):
                data_source = Storage("CFA Publications")
                scraper = Python("Web Scraper")
                s3_bucket = S3("S3 - Image & PDF Storage")
                snowflake_db = Snowflake("Snowflake Database")

                # Data flow from source through pipeline managed by Airflow
                data_source >> scraper
                scraper >> [s3_bucket, snowflake_db]

            # Indicate Airflow controls the entire flow
            airflow >> data_source

        # Part 2: Backend Processing and Interaction
        with Cluster("Backend Processing"):
            fastapi_app = Fastapi("FastAPI Backend")
            with Cluster("NVIDIA Services"):
                nvidia_summary = NvidiaIcon("NVIDIA Summary Generator")
                nvidia_rag = NvidiaIcon("NVIDIA Multi-modal RAG")

            fastapi_app >> [
                nvidia_summary,
                nvidia_rag,
            ]  # FastAPI backend interacts with NVIDIA services

        # Part 3: Client-Facing UI
        with Cluster("Client-Facing UI"):
            streamlit_ui = StreamlitIcon("Streamlit UI")
            with Cluster("UI Pages"):
                doc_selection_page = Action("Document Selection Page")
                summary_page = Action("On-the-Fly Summary Generation")
                qa_interface_page = Action("Interactive Q/A Interface")
                report_gen_page = Action("Report Generation Interface")

            streamlit_ui >> [
                doc_selection_page,
                summary_page,
                qa_interface_page,
                report_gen_page,
            ]  # Connect UI pages to main Streamlit interface

    return dia


if __name__ == "__main__":
    generate_assignment3_architecture()
