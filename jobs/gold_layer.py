from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def run_gold_layer():
    spark = SparkSession.builder.appName("Gold_Risk_Scoring").getOrCreate()
    
    # Load Silver Data
    df = spark.read.parquet("/opt/airflow/data/silver_table")

    # 1. AUM Segmentation (Assets Under Management)
    # High Net Worth (HNW) customers are high-priority for retention
    gold_df = df.withColumn(
        "aum_segment",
        F.when(F.col("balance") > 150000, "High Net Worth")
         .when(F.col("balance") > 50000, "Mass Affluent")
         .otherwise("Retail")
    )

    # 2. Silent Attrition Logic (Risk Scoring)
    # Risk factors: Inactive member, single product holding, and age
    gold_df = gold_df.withColumn(
        "risk_score",
        (F.when(F.col("active_member") == 0, 0.5).otherwise(0)) +
        (F.when(F.col("products_number") == 1, 0.3).otherwise(0)) +
        (F.when(F.col("age") > 50, 0.2).otherwise(0))
    )

    # 3. Retention Priority
    gold_df = gold_df.withColumn(
        "retention_priority",
        F.when(F.col("risk_score") >= 0.7, "URGENT")
         .when(F.col("risk_score") >= 0.4, "PROACTIVE")
         .otherwise("MONITOR")
    )

    # 4. Save to ABT (Analytical Base Table) partitioned by Segment
    # Senior DE practice: Partitioning by business-relevant columns
    gold_df.write.mode("overwrite").partitionBy("aum_segment").parquet("/opt/airflow/data/gold_abt_churn")
    print(">>> Gold Layer: ABT for Churn Retention Team Created.")

if __name__ == "__main__":
    run_gold_layer()