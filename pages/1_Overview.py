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

bg_image = get_base64_image(r"C:\Users\Alagu\Police_patrol\Assets\city-view.jpeg")

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


df = "uploaded_data"
os.makedirs(df, exist_ok=True)

uploaded_file = st.file_uploader("Upload cleaned dataset (CSV)", type=["csv"])
if uploaded_file:
    save_path = os.path.join(df, uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Saved to {save_path}")
    if st.button("Preview saved dataset"):
        df = pd.read_csv(save_path)
        st.dataframe(df.head())

if st.button("Use uploaded dataset as primary"):
    # copy into your Cleaned_data (overwrite)
    src = os.path.join(df, uploaded_file.name) if uploaded_file else None
    if src and os.path.exists(src):
        dest = os.path.join("Cleaned_data", "Feature_Engineering_Outputs", "emi_dataset_feature_engineered.csv")
        shutil.copy(src, dest)
        st.success(f"Dataset copied to {dest}. Now rerun training script to update models.")
    else:
        st.warning("No uploaded file found.")

st.metric("Total Crimes", len(df))
st.metric("Crime Types", df["Primary Type"].nunique())
st.metric("Locations", df["Location Description"].nunique())

st.subheader("Sample Crime Records")
st.dataframe(df.head())

