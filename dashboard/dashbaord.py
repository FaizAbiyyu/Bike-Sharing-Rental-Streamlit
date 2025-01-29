import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Load dataset
df = pd.read_csv("/mnt/data/all_data.csv")

# Konversi tanggal
df['dteday'] = pd.to_datetime(df['dteday'])

# Mengubah nama kolom
rename_cols = {
    'dteday': 'dateday',
    'yr_day': 'year',
    'mnth_day': 'month',
    'weathersit_day': 'weather_cond',
    'cnt_day': 'count'
}
df.rename(columns=rename_cols, inplace=True)

# Streamlit App
st.title('Bike Rental Dashboard 🚲')

# Sidebar Filter
min_date = df['dateday'].min()
max_date = df['dateday'].max()
with st.sidebar:
    st.text('Filter Data')
    start_date, end_date = st.date_input('Rentang Waktu', [min_date, max_date], min_value=min_date, max_value=max_date)

main_df = df[(df['dateday'] >= pd.Timestamp(start_date)) & (df['dateday'] <= pd.Timestamp(end_date))]

# Visualisasi Data
st.subheader('Distribusi Penggunaan Sepeda berdasarkan Musim')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='season_day', y='count', data=main_df, ax=ax)
st.pyplot(fig)

st.subheader('Penggunaan Sepeda pada Hari Kerja vs Akhir Pekan')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='workingday_day', y='count', data=main_df, ax=ax)
st.pyplot(fig)

st.subheader('Rata-rata Jumlah Penyewaan Sepeda per Jam')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt_hour', data=df.groupby('hr').mean().reset_index(), ax=ax)
st.pyplot(fig)

st.subheader('Tren Penggunaan Sepeda dari Tahun ke Tahun')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dateday', y='count', data=main_df, ax=ax)
st.pyplot(fig)

st.subheader('Pengaruh Suhu dan Kelembaban terhadap Penyewaan Sepeda')
fig, axes = plt.subplots(1, 3, figsize=(12, 5))
sns.scatterplot(x='temp_day', y='count', data=main_df, ax=axes[0])
sns.scatterplot(x='hum_day', y='count', data=main_df, ax=axes[1])
sns.scatterplot(x='windspeed_day', y='count', data=main_df, ax=axes[2])
st.pyplot(fig)

st.caption('Copyright (c) 2025 FaizAbiyyu')
