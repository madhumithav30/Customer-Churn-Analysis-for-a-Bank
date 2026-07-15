from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

def run_silver_layer():
    spark = SparkSession.builder.appName("Silver_PII_Masking").getOrCreate()

    # 1. Define Banking Schema (Senior DE practice: avoid inferSchema)
    schema = StructType([
        StructField("customer_id", IntegerType(), True),
        StructField("credit_score", IntegerType(), True),
        StructField("country", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("tenure", IntegerType(), True),
        StructField("balance", DoubleType(), True),
        StructField("products_number", IntegerType(), True),
        StructField("credit_card", IntegerType(), True),
        StructField("active_member", IntegerType(), True),
        StructField("estimated_salary", DoubleType(), True),
        StructField("churn", IntegerType(), True)
    ])

    # 2. Ingest Bronze Data (Raw CSV)
    raw_df = spark.read.csv("/opt/airflow/data/churn_data.csv", header=True, schema=schema)

    # 3. PIPEDA Compliance: Masking PII (Customer ID)
    # Hashing is essential for Canadian banking privacy standards
    silver_df = raw_df.withColumn("customer_id", F.sha2(F.col("customer_id").cast("string"), 256))

    # 4. Data Quality (DQ): Filtering invalid demographic data
    silver_df = silver_df.filter("age >= 18 AND age <= 100").fillna(0)

    # Write to Silver (Parquet format for performance)
    silver_df.write.mode("overwrite").parquet("/opt/airflow/data/silver_table")
    print(">>> Silver Layer: Cleansing and PII Masking Complete.")

if __name__ == "__main__":
    run_silver_layer()