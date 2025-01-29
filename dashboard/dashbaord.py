import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Load dataset
daily_df = pd.read_csv("dashboard/day.csv")
hr_df = pd.read_csv("dashboard/hour.csv")

# Konversi tanggal
daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])
hr_df['dteday'] = pd.to_datetime(hr_df['dteday'])

# Menghapus kolom yang tidak diperlukan
drop_col = ['instant']
daily_df.drop(columns=[col for col in drop_col if col in daily_df.columns], inplace=True)

# Mengubah nama kolom
daily_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Mengubah angka menjadi keterangan
daily_df['month'] = daily_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
daily_df['season'] = daily_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
daily_df['weekday'] = daily_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
daily_df['weather_cond'] = daily_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Streamlit App
st.title('Bike Rental Dashboard 🚲')

# Sidebar Filter
min_date = daily_df['dateday'].min()
max_date = daily_df['dateday'].max()
with st.sidebar:
    st.text('Filter Data')
    start_date, end_date = st.date_input('Rentang Waktu', [min_date, max_date], min_value=min_date, max_value=max_date)

main_df = daily_df[(daily_df['dateday'] >= str(start_date)) & (daily_df['dateday'] <= str(end_date))]

# Visualisasi Data
st.subheader('Distribusi Penggunaan Sepeda berdasarkan Musim')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='season', y='count', data=main_df, ax=ax)
st.pyplot(fig)

st.subheader('Penggunaan Sepeda pada Hari Kerja vs Akhir Pekan')
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='workingday', y='count', data=main_df, ax=ax)
st.pyplot(fig)

st.subheader('Rata-rata Jumlah Penyewaan Sepeda per Jam')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt', data=hr_df.groupby('hr').mean().reset_index(), ax=ax)
st.pyplot(fig)

st.subheader('Tren Penggunaan Sepeda dari Tahun ke Tahun')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='dateday', y='count', data=main_df, ax=ax)
st.pyplot(fig)

st.subheader('Pengaruh Suhu dan Kelembaban terhadap Penyewaan Sepeda')
fig, axes = plt.subplots(1, 3, figsize=(12, 5))
sns.scatterplot(x='temp', y='count', data=main_df, ax=axes[0])
sns.scatterplot(x='hum', y='count', data=main_df, ax=axes[1])
sns.scatterplot(x='windspeed', y='count', data=main_df, ax=axes[2])
st.pyplot(fig)

st.caption('Copyright (c) 2023')
