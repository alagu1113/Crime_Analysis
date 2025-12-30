import streamlit as st
import pandas as pd

import base64
#import streamlit as st

def set_crime_pattern_background(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        /* App background */
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Content overlay */
        .block-container {{
            background-color: rgba(2, 6, 23, 0.75); /* dark navy */
            padding: 2rem;
            border-radius: 14px;
        }}

        /* All text white */
        h1, h2, h3, h4, h5, h6, p, span, label {{
            color: white !important;
        }}

        /* Metrics */
        div[data-testid="metric-container"] {{
            background-color: rgba(0, 0, 0, 0.55);
            border-radius: 10px;
            padding: 12px;
        }}

        div[data-testid="metric-container"] * {{
            color: white !important;
        }}

        /* Charts background */
        canvas {{
            background-color: white !important;
            border-radius: 10px;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background-color: #020617;
        }}

        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(layout="wide")

set_crime_pattern_background(
    "/mount/src/crime_analysis/Assets/temp-patrol.jpg"
)

#st.title("⏱ Crime Pattern & Temporal Analysis")

st.title("⏱ Temporal Crime Patterns")

df = pd.read_csv("/mount/src/crime_analysis/Data/Crimes_Record_No_Outliers.csv")


df["date"] = pd.to_datetime(df["date"])

st.subheader("Crimes by hour")
hourly = df.groupby("hour").size()
st.line_chart(hourly)

st.subheader("Crimes by Day")
daily = df.groupby(df["date"].dt.day_name()).size()
st.bar_chart(daily)

import streamlit as st
import pandas as pd
import altair as alt

# Ensure Date column is datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# ---------------------------
# Crimes by Day
# ---------------------------
st.subheader("📊 Crimes by Day of Week")

daily = (
    df.groupby(df["date"].dt.day_name())
      .size()
      .reset_index(name="crime_count")
)

# Order days correctly
day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

daily["day"] = pd.Categorical(
    daily["date"],
    categories=day_order,
    ordered=True
)

daily = daily.sort_values("day")

# Identify max crime day
max_count = daily["crime_count"].max()
daily["severity"] = daily["crime_count"] / max_count

# ---------------------------
# Altair Bar Chart
# ---------------------------
chart = alt.Chart(daily).mark_bar().encode(
    x=alt.X("day:N", title="Day of Week"),
    y=alt.Y("crime_count:Q", title="Number of Crimes"),
    color=alt.condition(
        alt.datum.crime_count == max_count,
        alt.value("#ff0000"),  # 🔴 Red for max crime day
        alt.Color(
            "crime_count:Q",
            scale=alt.Scale(scheme="yelloworangebrown"),
            legend=alt.Legend(title="Crime Intensity")
        )
    ),
    tooltip=["day", "crime_count"]
).properties(
    height=420
)

st.altair_chart(chart, use_container_width=True)

# ---------------------------
# Highlight Max Crime Day
# ---------------------------
max_day = daily.loc[daily["crime_count"].idxmax(), "day"]

st.error(
    f"🚨 Highest crime occurs on **{max_day}** with **{max_count} incidents**"
)





