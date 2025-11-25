import streamlit as st
import pandas as pd
import altair as alt

# ============================
# DATASET (10 DATA GAME)
# ============================
data = {
    "game": [
        "Counter-Strike 2", "Dota 2", "PUBG", "Apex Legends", "GTA V",
        "Valorant", "Rust", "Elden Ring", "Baldur's Gate 3", "Fortnite"
    ],
    "genre": [
        "FPS", "MOBA", "Battle Royale", "Battle Royale", "Action",
        "FPS", "Survival", "RPG", "RPG", "Battle Royale"
    ],
    "rating": [9.1, 9.0, 8.7, 8.5, 9.5, 8.8, 8.1, 9.4, 9.6, 8.9],
    "ccu": [800000, 700000, 600000, 500000, 450000, 700000, 300000, 200000, 220000, 550000],
    "studio_country": [
        "US", "US", "South Korea", "US", "US",
        "US", "UK", "Japan", "US", "US"
    ],
    "cover": [
    "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg",
    "https://cdn.cloudflare.steamstatic.com/steam/apps/570/header.jpg",
    "https://cdn.cloudflare.steamstatic.com/steam/apps/578080/header.jpg",
    "https://cdn.cloudflare.steamstatic.com/steam/apps/1172470/header.jpg",
    "https://cdn.cloudflare.steamstatic.com/steam/apps/271590/header.jpg",
    "https://static.wikia.nocookie.net/valorant/images/2/20/Valorant_keyart.jpg",
    "https://cdn.cloudflare.steamstatic.com/steam/apps/252490/header.jpg",
    "https://cdn.cloudflare.steamstatic.com/steam/apps/1245620/header.jpg",
    "https://cdn.cloudflare.steamstatic.com/steam/apps/1086940/header.jpg",
    "https://cdn2.unrealengine.com/fortnite-chapter4-3840x2160-0915f7bd7460.jpg"
    ]

}

df = pd.DataFrame(data)

# Dummy data tren pemain 10 hari
trend = pd.DataFrame({
    "day": list(range(1, 11)),
    "players": [800000, 820000, 780000, 760000, 800000, 840000, 830000, 850000, 870000, 900000]
})

# Dummy area data (total waktu bermain per hari)
area_data = pd.DataFrame({
    "day": list(range(1, 11)),
    "play_time_hours": [100, 120, 130, 140, 160, 150, 170, 165, 180, 200]
})

# ============================
# STREAMLIT UI
# ============================

st.title("🎮 Top 10 Popular Games Analysis")
st.write("Visualisasi data 10 game terpopuler berdasarkan rating, genre, dan jumlah pemain (CCU).")

# Cover image gallery
st.subheader("Game Covers")
cols = st.columns(5)
for i, col in enumerate(cols):
    col.image(df["cover"][i], use_container_width=True)

cols2 = st.columns(5)
for i, col in enumerate(cols2):
    col.image(df["cover"][i+5], use_container_width=True)

st.divider()

# Dropdown
option = st.selectbox(
    "Pilih visualisasi:",
    ["Bar Chart - Pemain Terbanyak", 
     "Pie Chart - Distribusi Genre",
     "Line Chart - Tren Pemain 10 Hari",
     "Area Chart - Total Waktu Bermain",
     "Map - Negara Asal Studio"]
)

# ============================
# VISUALISASI
# ============================

# ---- BAR CHART ----
if option == "Bar Chart - Pemain Terbanyak":
    st.subheader("Bar Chart: Jumlah Pemain (CCU)")
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("game:N", sort="-y", title="Game"),
        y=alt.Y("ccu:Q", title="Concurrent Players"),
        tooltip=["game", "ccu", "rating", "genre"]
    )
    st.altair_chart(chart, use_container_width=True)

# ---- PIE CHART ----
elif option == "Pie Chart - Distribusi Genre":
    st.subheader("Pie Chart: Genre Game")

    genre_count = df["genre"].value_counts().reset_index()
    genre_count.columns = ["genre", "count"]

    pie = alt.Chart(genre_count).mark_arc().encode(
        theta="count",
        color="genre",
        tooltip=["genre", "count"]
    )
    st.altair_chart(pie, use_container_width=True)

# ---- LINE CHART ----
elif option == "Line Chart - Tren Pemain 10 Hari":
    st.subheader("Line Chart: Tren Pemain Harian")

    line = alt.Chart(trend).mark_line(point=True).encode(
        x=alt.X("day:O", title="Day"),
        y=alt.Y("players:Q", title="Players"),
        tooltip=["day", "players"]
    )
    st.altair_chart(line, use_container_width=True)

# ---- AREA CHART ----
elif option == "Area Chart - Total Waktu Bermain":
    st.subheader("Area Chart: Total Waktu Bermain per Hari")

    area = alt.Chart(area_data).mark_area(opacity=0.4).encode(
        x="day:O",
        y="play_time_hours:Q",
        tooltip=["day", "play_time_hours"]
    )
    st.altair_chart(area, use_container_width=True)

# ---- MAP ----
elif option == "Map - Negara Asal Studio (Opsional)":
    st.subheader("Peta: Negara Asal Pengembang Game")

    # Coordinates example (dummy)
    country_map = {
        "US": [37.0902, -95.7129],
        "Japan": [36.2048, 138.2529],
        "South Korea": [35.9078, 127.7669],
        "UK": [55.3781, -3.4360]
    }

    df["lat"] = df["studio_country"].apply(lambda x: country_map[x][0])
    df["lon"] = df["studio_country"].apply(lambda x: country_map[x][1])

    st.map(df[["lat", "lon"]], zoom=1)

