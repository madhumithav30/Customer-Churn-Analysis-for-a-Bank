FROM apache/airflow:2.7.1-python3.9

USER root
# Install OpenJDK-11 (Required for PySpark)
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME (Standard path for ARM64)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

USER airflow
RUN pip install pyspark