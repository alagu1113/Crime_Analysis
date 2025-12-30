import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Crime Data Overview",
    layout="wide"
)

# ---------------------------
# Load Background Image
# ---------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_image = get_base64_image("/mount/src/crime_analysis/Assets/city-view.jpeg")

# ---------------------------
# Apply CSS for Background, Main Text, and Sidebar
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

    /* Main container overlay for readability */
    .block-container {{
        background-color: rgba(0, 0, 0, 0.55);
        padding: 2rem;
        border-radius: 12px;
        color: #ffffff;
    }}

    /* Force all headers, paragraphs, lists, metric labels & numbers to white */
    h1, h2, h3, h4, h5, h6, p, li, div, td, th {{
        color: #ffffff !important;
    }}

    /* Streamlit metric number & label */
    .stMetricValue {{
        color: #ffffff !important;
    }}
    .stMetricLabel {{
        color: #ffffff !important;
    }}

    /* Streamlit table header & body */
    .css-1lcbmhc th {{
        color: #ffffff !important;
    }}
    .css-1lcbmhc td {{
        color: #ffffff !important;
    }}

    /* ---------------- Sidebar ---------------- */
    .css-1d391kg {{
        background-color: #000000 !important;  /* Black sidebar */
        color: #ffffff !important;
    }}
    .css-1d391kg * {{
        color: #ffffff !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# ---------------------------
# Main Page Content
# ---------------------------
st.title("📌 Crime Data Overview")

df = pd.read_csv("/mount/src/crime_analysis/Data/Crimes_Record_No_Outliers.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# ---------------------------
# Detect Columns SAFELY
# ---------------------------
crime_col = None
location_col = None

for col in df.columns:
    if "primary" in col and "type" in col:
        crime_col = col
    if "location" in col:
        location_col = col

if crime_col is None or location_col is None:
    st.error("❌ Required columns not found in dataset")
    st.write("Available columns:", df.columns.tolist())
    st.stop()

# ---------------------------
# Page Content
# ---------------------------
st.title("📌 Crime Data Overview")

st.metric("Total Crimes", len(df))
st.metric("Crime Types", df[crime_col].nunique())
st.metric("Locations", df[location_col].nunique())

st.subheader("📄 Sample Crime Records")
st.dataframe(df.head())
