import streamlit as st
import pandas as pd
import base64
from pathlib import Path

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="Crime Data Overview",
    layout="wide"
)

# ---------------------------
# Load Background Image (RELATIVE PATH)
# ---------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_image = get_base64_image("Assets/city-view.jpeg")

# ---------------------------
# Apply CSS (Background + White Text + Black Sidebar)
# ---------------------------
st.markdown(
    f"""
    <style>
    /* Background */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Main content overlay */
    .block-container {{
        background-color: rgba(0, 0, 0, 0.60);
        padding: 2rem;
        border-radius: 14px;
    }}

    /* Force all text white */
    h1, h2, h3, h4, h5, h6, p, span, label, li, div {{
        color: #ffffff !important;
    }}

    /* Metrics */
    [data-testid="stMetricValue"] {{
        color: #ffffff !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: #ffffff !important;
    }}

    /* Dataframe */
    .stDataFrame {{
        color: #ffffff !important;
    }}

    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background-color: #000000;
    }}
    section[data-testid="stSidebar"] * {{
        color: #ffffff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Load Data (RELATIVE PATH)
# ---------------------------
df = pd.read_csv("data/Crimes_Record_No_Outliers.csv")

# ---------------------------
# Page Content
# ---------------------------
st.title("📌 Crime Data Overview")

st.metric("Total Crimes", len(df))
st.metric("Crime Types", df["Primary Type"].nunique())
st.metric("Locations", df["Location Description"].nunique())

st.subheader("📄 Sample Crime Records")
st.dataframe(df.head())
