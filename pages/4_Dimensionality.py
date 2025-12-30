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
# Load Data
# ---------------------------
df = pd.read_csv("Data/Crimes_Record_No_Outliers.csv")
st.write("Dataset shape:", df.shape)

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
st.sidebar.header("Model Settings")

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
# PCA Scatter (Streamlit Native)
# ---------------------------
st.subheader("📈 PCA Cluster Visualization")

pca_df = pd.DataFrame({
    "PCA_1": X_pca[:, 0],
    "PCA_2": X_pca[:, 1],
    "Cluster": labels.astype(str)
})

st.scatter_chart(
    pca_df,
    x="PCA_1",
    y="PCA_2",
    color="Cluster"
)

# ---------------------------
# Explained Variance
# ---------------------------
st.subheader("📊 PCA Explained Variance")

explained_df = pd.DataFrame({
    "Component": [f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],
    "Variance": pca.explained_variance_ratio_
})

st.bar_chart(explained_df.set_index("Component"))

# ---------------------------
# Cluster Sizes
# ---------------------------
st.subheader("📌 Cluster Sizes")

cluster_counts = (
    pd.Series(labels)
    .value_counts()
    .sort_index()
    .rename("Crime Count")
)

st.dataframe(cluster_counts)
