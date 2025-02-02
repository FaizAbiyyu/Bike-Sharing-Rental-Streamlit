import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Load dataset
df = pd.read_csv("alldata.csv")

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

# Pastikan 'cnt_hour' bertipe numerik
df['cnt_hour'] = pd.to_numeric(df['cnt_hour'], errors='coerce')

# Mengelompokkan dan menghitung rata-rata hanya untuk kolom numerik
df_grouped = df.groupby('hr').mean(numeric_only=True).reset_index()

st.subheader('Rata-rata Jumlah Penyewaan Sepeda per Jam')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='hr', y='cnt_hour', data=df_grouped, ax=ax)
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

# Pastikan kolom 'dteday' ada dan bertipe datetime
if 'dateday' not in df.columns:
    st.error("Kolom 'dateday' tidak ditemukan dalam dataset!")
else:
    df['dateday'] = pd.to_datetime(df['dateday'], errors='coerce')

    # Tentukan max_date (misalnya, hari terakhir dalam dataset)
    max_date = df['dateday'].max()

    # Hitung RFM
    rfm = df.groupby('dateday').agg(
        Frequency=('dateday', 'count'),
        Monetary=('count', 'sum')
    ).reset_index()

    rfm['Recency'] = (max_date - rfm['dateday']).dt.days

    # Menampilkan dataframe hasil RFM
    st.subheader("Hasil Perhitungan RFM")
    st.write(rfm.head())

    # Visualisasi RFM
    st.subheader("Visualisasi RFM")
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))
    colors = ["#72BCD4"] * 5

    sns.barplot(y="Recency", x="dateday", data=rfm.sort_values(by="Recency", ascending=True).head(5), palette=colors, ax=ax[0])
    ax[0].set_title("By Recency (days)", fontsize=18)
    ax[0].tick_params(axis='x', rotation=45)

    sns.barplot(y="Frequency", x="dateday", data=rfm.sort_values(by="Frequency", ascending=False).head(5), palette=colors, ax=ax[1])
    ax[1].set_title("By Frequency", fontsize=18)
    ax[1].tick_params(axis='x', rotation=45)

    sns.barplot(y="Monetary", x="dateday", data=rfm.sort_values(by="Monetary", ascending=False).head(5), palette=colors, ax=ax[2])
    ax[2].set_title("By Monetary", fontsize=18)
    ax[2].tick_params(axis='x', rotation=45)

    plt.suptitle("Best Rental Days Based on RFM Parameters", fontsize=20)
    st.pyplot(fig)

st.caption('Copyright (c) 2025 FaizAbiyyu')
