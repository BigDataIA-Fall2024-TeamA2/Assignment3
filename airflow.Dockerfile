FROM apache/airflow:2.10.2

USER root


# custom, needed for other reqs
RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*


# Set an alias for chromium to make it easier to run
RUN ln -s /usr/bin/chromium-browser /usr/bin/chromium

#RUN pip install --no-cache-dir --upgrade pip
#
#RUN pip install --no-cache-dir boto3 selenium webdriver-manager snowflake-connector-python
#
##USER airflow
