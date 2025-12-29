import streamlit as st
import base64
from pathlib import Path

# ---------------------------
# Page Config (ONLY ONCE)
# ---------------------------
st.set_page_config(
    page_title="Crime Analytics Platform",
    layout="wide"
)

# ---------------------------
# Page Content
# ---------------------------
st.title("🚓 Crime Analytics & Clustering Platform")

st.markdown("""
### 🔍 Features
- 📍 **Geographic crime heatmaps**
- ⏱ **Temporal crime pattern analysis**
- 📊 **PCA & UMAP dimensionality reduction**
- 🧠 **MLflow model monitoring**
- 🚓 **Hotspot policing recommendations**
""")

st.success("🔐 Data-driven policing for smarter crime prevention")

