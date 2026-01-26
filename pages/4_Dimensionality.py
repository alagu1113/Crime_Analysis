import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------
# Page Setup
# ---------------------------
st.set_page_config(layout="wide")
st.title("📊 PCA + KMeans Crime Clustering (No sklearn)")

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

X = X.values

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
# Standard Scaling (Manual)
# ---------------------------
mean = X.mean(axis=0)
std = X.std(axis=0)
X_scaled = (X - mean) / std

# ---------------------------
# PCA using SVD (No sklearn)
# ---------------------------
U, S, Vt = np.linalg.svd(X_scaled, full_matrices=False)
X_pca = np.dot(X_scaled, Vt.T[:, :n_components])

explained_variance_ratio = (S**2) / np.sum(S**2)
explained_variance_ratio = explained_variance_ratio[:n_components]

# ---------------------------
# Simple KMeans (Manual)
# ---------------------------
def kmeans(X, k, max_iters=100):
    np.random.seed(42)
    centroids = X[np.random.choice(len(X), k, replace=False)]

    for _ in range(max_iters):
        distances = np.linalg.norm(X[:, None] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)

        new_centroids = np.array([
            X[labels == i].mean(axis=0) if np.any(labels == i) else centroids[i]
            for i in range(k)
        ])

        if np.allclose(centroids, new_centroids):
            break

        centroids = new_centroids

    return labels, centroids

labels, centroids = kmeans(X_pca, n_clusters)

# ---------------------------
# PCA Scatter Plot
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
    "Component": [f"PC{i+1}" for i in range(len(explained_variance_ratio))],
    "Variance": explained_variance_ratio
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
