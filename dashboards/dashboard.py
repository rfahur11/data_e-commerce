import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul dashboard
st.title('Dashboard Analisis Data E-Commerce')

# Sidebar untuk pilihan menu
st.sidebar.title('Menu Navigasi')
pilihan = st.sidebar.radio('Pilih Analisis:', 
    ('Data Mentah', 'Analisis Kategori Produk', 'Produk dengan Penilaian Tertinggi'))

# Membaca data
data = pd.read_csv('all_data.csv')

if pilihan == 'Data Mentah':
    # Menampilkan data mentah
    st.subheader('Data Mentah')
    st.write(data.head())

elif pilihan == 'Analisis Kategori Produk':
    # Analisis kategori produk yang paling banyak dan paling sedikit dibeli
    st.subheader('Analisis Kategori Produk')
    kategori_count = data['product_category_name_english'].value_counts()
    kategori_terbanyak = kategori_count.idxmax()
    kategori_tersedikit = kategori_count.idxmin()
    st.write(f"Kategori produk yang paling banyak dibeli adalah: {kategori_terbanyak}")
    st.write(f"Kategori produk yang paling sedikit dibeli adalah: {kategori_tersedikit}")

    # Grafik batang untuk kategori produk
    st.subheader('Grafik Jumlah Pembelian per Kategori Produk')
    fig, ax = plt.subplots()
    kategori_count.plot(kind='bar', ax=ax)
    st.pyplot(fig)

elif pilihan == 'Produk dengan Penilaian Tertinggi':
    # Analisis produk dengan penilaian tertinggi
    st.subheader('Produk dengan Penilaian Tertinggi')
    penilaian_produk = data.groupby(['product_id', 'product_category_name_english'])['review_score'].mean()
    penilaian_tertinggi = penilaian_produk.sort_values(ascending=False).head(10)
    penilaian_tertinggi_kategori = penilaian_tertinggi.index.get_level_values('product_category_name_english').tolist()

    # Grafik batang untuk 10 penilaian tertinggi dengan nama kategori produk
    st.subheader('Grafik 10 Produk dengan Penilaian Tertinggi')
    fig, ax = plt.subplots()
    penilaian_tertinggi.plot(kind='bar', ax=ax)
    ax.set_xticklabels(penilaian_tertinggi_kategori, rotation=45)
    st.pyplot(fig)

    # Menampilkan kategori produk dengan 10 penilaian tertinggi
    st.subheader('Kategori Produk dengan 10 Penilaian Tertinggi')
    for index, (product_id, category_name) in enumerate(zip(penilaian_tertinggi.index.get_level_values('product_id'), penilaian_tertinggi_kategori), start=1):
        product_score = penilaian_produk.loc[(product_id, category_name)]
        st.write(f"{index}. {category_name} (ID Produk: {product_id}, Skor Rata-Rata: {product_score:.2f})")
