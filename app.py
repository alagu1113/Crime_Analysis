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
# Load background image (CLOUD SAFE)
# ---------------------------
def get_base64_image(image_path):
    image_path = Path(image_path)
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Relative path (IMPORTANT for cloud)
bg_image = get_base64_image("Assets/police_patrol.jpg")

# ---------------------------
# Apply CSS Background
# ---------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Dark overlay for readability */
    .block-container {{
        background-color: rgba(0, 0, 0, 0.55);
        padding: 2rem;
        border-radius: 12px;
    }}

    /* All text white */
    h1, h2, h3, h4, h5, h6, p, li, span {{
        color: #ffffff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
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
