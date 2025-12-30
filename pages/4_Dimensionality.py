import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# ---------------------------
# Streamlit Page Setup
# ---------------------------
st.set_page_config(layout="wide")
st.title("📊 PCA + KMeans Crime Clustering")

# ---------------------------
# Load Data
# ---------------------------
df = pd.read_csv("/mount/src/crime_analysis/Data/Crimes_Record_No_Outliers.csv")

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
# Visualization
# ---------------------------
st.subheader("📈 PCA Cluster Visualization")

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=labels,
    alpha=0.7
)

ax.set_xlabel("PCA Component 1")
ax.set_ylabel("PCA Component 2")
ax.set_title("Crime Clusters (PCA Space)")

st.pyplot(fig)

# ---------------------------
# Explained Variance
# ---------------------------
st.subheader("📊 PCA Explained Variance")

explained_variance = pca.explained_variance_ratio_
st.bar_chart(explained_variance)

# ---------------------------
# Cluster Summary
# ---------------------------
st.subheader("📌 Cluster Sizes")

cluster_counts = pd.Series(labels).value_counts().sort_index()
st.write(cluster_counts)
#
import numpy as np

st.subheader("📈 PCA Cluster Visualization")

fig, ax = plt.subplots(figsize=(8, 6))

unique_labels = np.unique(labels)

for label in unique_labels:
    ax.scatter(
        X_pca[labels == label, 0],
        X_pca[labels == label, 1],
        label=f"Cluster {label}",
        alpha=0.7
    )

ax.set_xlabel("PCA Component 1")
ax.set_ylabel("PCA Component 2")
ax.set_title("Crime Clusters in PCA Space")
ax.legend(title="Clusters")

st.pyplot(fig)

st.subheader("📊 Crime Count per Cluster")

cluster_counts = pd.Series(labels).value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(6, 4))

bars = ax2.bar(
    cluster_counts.index.astype(str),
    cluster_counts.values
)

ax2.set_xlabel("Cluster Label")
ax2.set_ylabel("Number of Crimes")
ax2.set_title("Crime Distribution Across Clusters")

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        height,
        int(height),
        ha="center",
        va="bottom"
    )

st.pyplot(fig2)


