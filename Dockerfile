FROM apache/airflow:2.7.1-python3.9

USER root
# Install Java 17 for AMD64 (Codespaces architecture)
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-17-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set Java Home
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

USER airflow
RUN pip install --no-cache-dir pyspark
RUN pip install --no-cache-dir pyspark pandas seaborn matplotlib
