import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from PIL import Image

# Set Streamlit page config
st.set_page_config(page_title="Lunar Anomalies Explorer", layout="wide")

with open("C:\\Users\\saeem\\Desktop\\Lunar\\assets\styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load data
df = pd.read_csv(r"C:\Users\saeem\Desktop\Lunar\cleaned_lunar_anomalies.csv")
with open(r"C:\Users\saeem\Desktop\Lunar\app\cluster_words.json", "r") as f:
    cluster_words = json.load(f)


# --- Ensure proper datetime ---
if 'Date' not in df.columns:
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    df['Month'] = df['Month'].astype(str).str.strip().str.lower().map(month_map)
    df['Day'] = df['Day'].clip(1, 28)
    df['Date'] = pd.to_datetime(dict(year=df['Year'], month=df['Month'], day=df['Day']), errors='coerce')
df.dropna(subset=['Date'], inplace=True)



# Title
st.title("🌕 Chronicles of the Moon: Lunar Anomaly Explorer")

# Sidebar filters
st.sidebar.header("🔎 Filter Anomalies")
year_range = st.sidebar.slider("Select Year Range:", int(df['Year'].min()), int(df['Year'].max()), (1700, 1900))
locations = st.sidebar.multiselect("Filter by Location", options=df["Location"].dropna().unique())

# Apply filters
filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
if locations:
    filtered_df = filtered_df[filtered_df['Location'].isin(locations)]

# Main PCA Cluster Scatter Plot
st.subheader(" PCA Visualization of Anomaly Clusters")
fig, ax = plt.subplots()
scatter = ax.scatter(
    filtered_df["PC1"], filtered_df["PC2"],
    c=filtered_df["Cluster"], cmap="tab10", alpha=0.7
)
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")
ax.set_title("2D Clustering of Lunar Anomalies")
st.pyplot(fig)


# Cluster Info Section
st.subheader("📌 Cluster Summary")

for cluster_id, words in cluster_words.items():
    st.markdown(f"**Cluster {cluster_id}** – Top Words: _{', '.join(words)}_")
    try:
        img_path = f"C:\\Users\\saeem\\Desktop\\Lunar\\assets\\wordcloud_cluster_{cluster_id}.png"
        image = Image.open(img_path)
        st.image(image, caption=f"Wordcloud for Cluster {cluster_id}", use_column_width=True)
    except:
        st.warning(f"Wordcloud for Cluster {cluster_id} not found.")



# Dataset Explorer
st.subheader("🧮 Dataset Explorer")

search_term = st.text_input("Search anomaly descriptions:")
explore_df = filtered_df.copy()
if search_term:
    explore_df = explore_df[explore_df["Description"].str.contains(search_term, case=False, na=False)]

st.dataframe(explore_df[["Year", "Month", "Day", "Location", "Description", "Cluster"]].reset_index(drop=True))


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
# Timeline chart of anomalies by date
fig = px.histogram(df, x='Date', nbins=100, title='Lunar Anomalies Over Time')
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Number of Anomalies',
    bargap=0.1,
)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

# Load mission data
import json
missions_path = r"C:\Users\saeem\Desktop\Lunar\app\moon_missions.json"
missions = []

try:
    with open(missions_path, "r", encoding="utf-8") as f:
        missions = json.load(f)
except json.JSONDecodeError as e:
    import streamlit as st
    st.error(f"❌ Error loading JSON: {e}")
    missions = []
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")


# Add mission markers to timeline plot
for mission in missions:
    mission_date = pd.to_datetime(mission["date"]).to_pydatetime()
fig.add_vline(
    x=mission_date,
    line_color="red",
    line_dash="dot"
)

fig.add_annotation(
    x=mission_date,
    y=0,  # Adjust as needed
    text=mission["name"],
    showarrow=True,
    arrowhead=1,
    yshift=10
)


# Display the figure
st.plotly_chart(fig, use_container_width=True)