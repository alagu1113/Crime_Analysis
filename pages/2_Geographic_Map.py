import base64
import streamlit as st
import pandas as pd
import pydeck as pdk
import os

# ---------------------------
# MAPBOX TOKEN (REQUIRED)
# ---------------------------
os.environ["MAPBOX_API_KEY"] = os.getenv("MAPBOX_API_KEY", "")

st.set_page_config(layout="wide")
st.title("🗺 Geographic Crime Heatmap (Balanced Sample)")

# ---------------------------
# Load CSV
# ---------------------------
df = pd.read_csv("/mount/src/crime_analysis/pages/Crimes_Record_No_Outliers.csv")

df.columns = df.columns.str.strip().str.lower()
#st.write("Columns:", df.columns.tolist())

# ---------------------------
# Category Column
# ---------------------------
if "primary type" in df.columns:
    category_col = "primary type"
elif "primary_type" in df.columns:
    category_col = "primary_type"
else:
    st.error("❌ No crime category column found")
    st.stop()

# ---------------------------
# Latitude / Longitude
# ---------------------------
rename_map = {
    "lat": "latitude",
    "lon": "longitude",
    "lng": "longitude"
}
df.rename(columns=rename_map, inplace=True)

if "latitude" not in df.columns or "longitude" not in df.columns:
    st.error("❌ latitude / longitude columns missing")
    st.stop()

df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
df = df.dropna(subset=["latitude", "longitude", category_col])

# ---------------------------
# Balanced Sampling
# ---------------------------
SAMPLE_PER_CATEGORY = 300

df_sampled = (
    df.groupby(category_col, group_keys=False)
      .apply(lambda x: x.sample(
          n=min(len(x), SAMPLE_PER_CATEGORY),
          random_state=42
      ))
)

if df_sampled.empty:
    st.error("❌ No data available after sampling")
    st.stop()

st.success(f"Sampled rows: {len(df_sampled)}")

# ---------------------------
# View State (IMPORTANT)
# ---------------------------
view_state = pdk.ViewState(
    latitude=float(df_sampled["latitude"].mean()),
    longitude=float(df_sampled["longitude"].mean()),
    zoom=11,
    pitch=40,
    bearing=0
)

# ---------------------------
# HEATMAP LAYER (IMPROVED)
# ---------------------------
heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=df_sampled,
    get_position="[longitude, latitude]",
    get_weight=1,
    radius_pixels=40,
    intensity=1.0,
    threshold=0.05
)

# ---------------------------
# Render Map (FIXED)
# ---------------------------
deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v11",
    initial_view_state=view_state,
    layers=[heatmap_layer],
    tooltip={
        "text": "{primary type}"
    }
)

st.pydeck_chart(deck)
# Identify location column
possible_cols = ["location", "district", "beat", "ward", "area"]

location_col = None
for col in possible_cols:
    if col in df.columns:
        location_col = col
        break

if location_col is None:
    st.warning("No location name column found")
else:
    max_location = (
        df[location_col]
        .value_counts()
        .idxmax()
    )

    max_count = df[location_col].value_counts().max()

    st.metric(
        label="📍 Location with Maximum Crimes",
        value=max_location
    )

    st.write(f"Total Crimes: {max_count}")
######################
# ---------------------------
# Identify Max Crime Location (Coordinates)
# ---------------------------

# Create geo bins (adjust precision if needed)
df["lat_bin"] = df["latitude"].round(4)
df["lon_bin"] = df["longitude"].round(4)

# Count crimes per geo location
location_counts = (
    df.groupby(["lat_bin", "lon_bin"])
      .size()
      .reset_index(name="crime_count")
)

# Find location with maximum crimes
max_location = location_counts.loc[
    location_counts["crime_count"].idxmax()
]

max_lat = float(max_location["lat_bin"])
max_lon = float(max_location["lon_bin"])
max_count = int(max_location["crime_count"])

# ---------------------------
st.markdown(
    """
    <style>
    /* Force all text to white */
    html, body, [class*="css"]  {
        color: white !important;
    }

    /* Metrics text */
    div[data-testid="metric-container"] {
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 10px;
        padding: 10px;
    }

    div[data-testid="metric-container"] * {
        color: white !important;
    }

    /* DataFrame text */
    .stDataFrame, .stDataFrame * {
        color: white !important;
    }

    /* Table headers */
    thead tr th {
        color: white !important;
        background-color: rgba(0,0,0,0.7);
    }

    /* Table rows */
    tbody tr td {
        color: white !important;
        background-color: rgba(0,0,0,0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ---------------------------
# Display Results
# ---------------------------

st.markdown(
    "<h2 style='color:#ff4b4b;'>📍 Maximum Crime Location</h2>",
    unsafe_allow_html=True
)

st.metric("Latitude", f"{max_lat}")
st.metric("Longitude", f"{max_lon}")
st.metric("Crime Count", f"{max_count}")

# Filter records at max crime location
hotspot_crimes = df[
    (df["lat_bin"] == max_lat) &
    (df["lon_bin"] == max_lon)
]

crime_type_counts = (
    hotspot_crimes[category_col]
    .value_counts()
    .reset_index()
)

crime_type_counts.columns = ["Crime Type", "Count"]

top_crime_type = crime_type_counts.iloc[0]["Crime Type"]
top_crime_count = int(crime_type_counts.iloc[0]["Count"])

st.markdown(
    "<h3 style='color:#ff4b4b;'>🚨 Crime Types at Highest Crime Location</h3>",
    unsafe_allow_html=True
)

st.metric("Most Frequent Crime Type", top_crime_type)
st.metric("Occurrences", f"{top_crime_count}")

st.dataframe(
    crime_type_counts,
    use_container_width=True
)

# ---------------------------
# POLICE PATROL RECOMMENDATION
# ---------------------------

st.subheader("🚓 Hotspot Policing Recommendation")

st.warning(
    f"""
    ⚠️ **High Crime Hotspot Identified**

    📍 **Location Coordinates**
    - Latitude: **{max_lat}**
    - Longitude: **{max_lon}**
    - Total Crimes Reported: **{max_count}**

    🔴 **Dominant Crime Type**
    - **{top_crime_type}**  
    - Occurrences: **{top_crime_count}**

    🛑 **Recommended Police Action**
    - Declare this area as a **Crime Hotspot**
    - Increase **police patrol frequency**
    - Deploy **foot patrols and mobile patrol units**
    - Schedule patrols during **high-risk time periods**
    - Focus enforcement on **{top_crime_type} related offenses**

    📌 **This recommendation is based on spatial crime density analysis and crime frequency patterns.**
    """
)



