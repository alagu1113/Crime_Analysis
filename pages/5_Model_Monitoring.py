import streamlit as st
import mlflow

st.title("🧠 Model Performance Monitoring")

mlflow.set_tracking_uri("file:./mlruns")

client = mlflow.tracking.MlflowClient()
exp = client.get_experiment_by_name("Crime_Clustering_Experiments")

runs = client.search_runs(exp.experiment_id)

st.subheader("Recent Runs")

for run in runs[:5]:
    st.markdown(f"""
    **Run ID:** {run.info.run_id}  
    Silhouette Score: `{run.data.metrics.get('silhouette_score', 'N/A')}`  
    Davies-Bouldin: `{run.data.metrics.get('davies_bouldin_index', 'N/A')}`  
    """)
