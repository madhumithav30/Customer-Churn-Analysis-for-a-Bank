import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_plots():
    # 1. Load the Gold ABT (Partitioned Parquet)
    path = "/opt/airflow/data/gold_abt_churn"
    if not os.path.exists(path):
        print("Data not found. Please run the pipeline first.")
        return
    
    df = pd.read_parquet(path)

    # Set the visual style
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(12, 6))

    # 2. Plot: Retention Priority by Wealth Segment
    # This shows the business exactly where the risk is
    ax = sns.countplot(data=df, x='aum_segment', hue='retention_priority', 
                       hue_order=['MONITOR', 'PROACTIVE', 'URGENT'],
                       palette={'MONITOR': 'green', 'PROACTIVE': 'orange', 'URGENT': 'red'})

    plt.title('Customer Retention Priority by Wealth Segment', fontsize=16)
    plt.xlabel('Wealth Segment (AUM)', fontsize=12)
    plt.ylabel('Number of Customers', fontsize=12)
    plt.legend(title='Retention Priority')

    # 3. Save the plot to the images folder for GitHub
    output_path = "/opt/airflow/jobs/retention_analytics.png"
    plt.savefig(output_path)
    print(f"Plot saved successfully to {output_path}")

if __name__ == "__main__":
    create_plots()