import streamlit as st
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# ---------------------------
# Page Setup
# ---------------------------
st.set_page_config(layout="wide")
st.title("📊 PCA + KMeans Crime Clustering")

# ---------------------------
# Load Data (CLOUD SAFE PATH)
# ---------------------------
DATA_PATH = "Data/Crimes_Record_No_Outliers.csv"
df = pd.read_csv(DATA_PATH)

st.write("📄 Dataset shape:", df.shape)

# ---------------------------
# Select Numeric Features
# ---------------------------
X = df.select_dtypes(include="number")

if X.shape[1] < 2:
    st.error("❌ Not enough numeric features for PCA")
    st.stop()

# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.header("⚙️ Model Settings")

n_components = st.sidebar.slider(
    "PCA Components",
    min_value=2,
    max_value=min(6, X.shape[1]),
    value=2
)

n_clusters = st.sidebar.slider(
    "KMeans Clusters",
    min_value=2,
    max_value=10,
    value=4
)

# ---------------------------
# Scaling
# ---------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------------------
# PCA
# ---------------------------
pca = PCA(n_components=n_components, random_state=42)
X_pca = pca.fit_transform(X_scaled)

# ---------------------------
# KMeans
# ---------------------------
kmeans = KMeans(
    n_clusters=n_clusters,
    random_state=42,
    n_init=10
)

labels = kmeans.fit_predict(X_pca)

# ---------------------------
# PCA Scatter Plot (STREAMLIT)
# ---------------------------
st.subheader("📈 PCA Cluster Visualization")

pca_df = pd.DataFrame({
    "PCA 1": X_pca[:, 0],
    "PCA 2": X_pca[:, 1],
    "Cluster": labels.astype(str)
})

st.scatter_chart(
    pca_df,
    x="PCA 1",
    y="PCA 2",
    color="Cluster"
)

# ---------------------------
# Explained Variance
# ---------------------------
st.subheader("📊 PCA Explained Variance Ratio")

explained_variance = pd.DataFrame({
    "Component": [f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],
    "Variance Ratio": pca.explained_variance_ratio_
})

st.bar_chart(explained_variance.set_index("Component"))

# ---------------------------
# Cluster Size Summary
# ---------------------------
st.subheader("📌 Crime Count per Cluster")

cluster_counts = pd.Series(labels).value_counts().sort_index()
cluster_df = pd.DataFrame({
    "Cluster": cluster_counts.index.astype(str),
    "Crimes": cluster_counts.values
})

st.bar_chart(cluster_df.set_index("Cluster"))
