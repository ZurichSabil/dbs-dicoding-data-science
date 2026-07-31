import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Load data
new_hour_df = pd.read_csv("new_hour_df.csv")
new_day_df = pd.read_csv("new_day_df.csv")

all_df = pd.merge(new_hour_df, new_day_df, on="dteday")
all_df = all_df.rename(columns={
    'yr_x': 'yr',
    'cnt_x': 'cnt'
})

# Convert date
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
min_date = all_df['dteday'].min().date()
max_date = all_df['dteday'].max().date()

# Sidebar filter
st.sidebar.header("Filter")
with st.sidebar:
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Handle date input
if isinstance(date_range, (list, tuple)):
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]
else:
    start_date = end_date = date_range

# MAIN FILTER
main_df = all_df[
    (all_df['dteday'] >= pd.to_datetime(start_date)) &
    (all_df['dteday'] <= pd.to_datetime(end_date))
]

# 🔥 HANDLE DATA KOSONG GLOBAL
if main_df.empty:
    st.error("Tidak ada data pada rentang waktu yang dipilih")
    st.stop()

# =========================
# FUNCTIONS
# =========================

def countAverageBicycle(df):
    day_2012 = df[df['yr'] == 1]

    if day_2012.empty:
        return None

    avg = day_2012.groupby(['mnth', 'workingday'])['cnt'].mean().reset_index()
    
    pivot = avg.pivot(index='mnth', columns='workingday', values='cnt')

    pivot = pivot.reindex(columns=[0,1])
    pivot.columns = ['Holiday/Weekend', 'Working Day']

    return pivot


def plot_averageBicycle(pivot_df):
    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(pivot_df.index, pivot_df['Working Day'], marker='o', label='Working Day')
    ax.plot(pivot_df.index, pivot_df['Holiday/Weekend'], marker='o', label='Holiday/Weekend')

    ax.set_title('Rata-rata Peminjaman Sepeda per Bulan (2012)')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Peminjaman')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)


def countWeatherResult(df):
    day_2012 = df[df['yr'] == 1]

    if day_2012.empty:
        return None

    result = day_2012.groupby('weathersit')['cnt'].sum().reset_index()
    return result.sort_values(by='cnt', ascending=False)


def plot_weatherResult(df):
    if df is None or df.empty:
        st.warning("Data cuaca tidak tersedia")
        return

    weather_labels = {
        1: 'Clear / Partly Cloudy',
        2: 'Mist / Cloudy',
        3: 'Light Rain / Snow'
    }

    df = df[df['weathersit'].isin([1,2,3])].copy()
    df['label'] = df['weathersit'].map(weather_labels)

    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(df['label'], df['cnt'])

    ax.set_title('Total Peminjaman Berdasarkan Cuaca')
    ax.grid(axis='y')

    st.pyplot(fig)


def compareHours(df):
    h2011 = df[df['yr'] == 0]
    h2012 = df[df['yr'] == 1]

    if h2011.empty or h2012.empty:
        return None

    h2011 = h2011.groupby('hr')['cnt'].sum().reset_index()
    h2012 = h2012.groupby('hr')['cnt'].sum().reset_index()

    h2011.rename(columns={'cnt': '2011'}, inplace=True)
    h2012.rename(columns={'cnt': '2012'}, inplace=True)

    return pd.merge(h2011, h2012, on='hr')


def plot_compareHours(df):
    if df is None or df.empty:
        st.warning("Data jam tidak tersedia")
        return

    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(df['hr'], df['2011'], marker='o', label='2011')
    ax.plot(df['hr'], df['2012'], marker='o', label='2012')

    ax.set_title('Perbandingan per Jam')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)


def add_time_group(df):
    def kategori(h):
        if 5 <= h < 10: return 'Pagi'
        elif 10 <= h < 15: return 'Siang'
        elif 15 <= h < 19: return 'Sore'
        else: return 'Malam'
    
    df = df.copy()
    df['time_group'] = df['hr'].apply(kategori)
    return df


def plot_time_group(df):
    if df.empty:
        st.warning("Data clustering tidak tersedia")
        return

    result = df.groupby('time_group')['cnt'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(8,5))
    ax.bar(result['time_group'], result['cnt'])

    ax.set_title('Peminjaman Berdasarkan Waktu')
    ax.grid(axis='y')

    st.pyplot(fig)

# =========================
# DASHBOARD
# =========================

st.title("Dashboard Bike Sharing")

home = main_df.groupby('dteday')['cnt'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total", f"{home.sum():,}")
col2.metric("Rata-rata", f"{home.mean():.0f}")
col3.metric("Tertinggi", f"{home.max():,}")

st.write("Jumlah data setelah filter:", main_df.shape)

tab1, tab2, tab3, tab4 = st.tabs([
    "📅 Bulanan",
    "🌦️ Cuaca",
    "⏱️ Jam",
    "🧠 Clustering"
])

with tab1:
    st.subheader("Bulanan")
    pivot_df = countAverageBicycle(main_df)

    if pivot_df is None or pivot_df.empty:
        st.warning("Data tidak tersedia untuk filter ini")
    else:
        plot_averageBicycle(pivot_df)

with tab2:
    st.subheader("Cuaca")
    weather = countWeatherResult(main_df)
    plot_weatherResult(weather)

with tab3:
    st.subheader("Per Jam")
    hour_df = compareHours(main_df)
    plot_compareHours(hour_df)

with tab4:
    st.subheader("Clustering Waktu")
    df_time = add_time_group(main_df)
    plot_time_group(df_time)