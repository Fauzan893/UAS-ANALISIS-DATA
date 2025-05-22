import streamlit as st
import pandas as pd
import numpy as np
import io
import altair as alt
import matplotlib.pyplot as px

st.set_page_config(page_title="Analisis Produksi Jagung & Kedelai 2015", layout="wide")

# Sidebar
st.sidebar.title("ℹ️ Informasi Kelompok")
st.sidebar.markdown(
    """
    **Mata Kuliah:** Algoritma dan Pemrograman Dasar  
    **Kelompok:** 2  
    """
)

# Anggota Kelompok
selected_member = st.sidebar.selectbox(
    "👥 Pilih Anggota Kelompok",
    [
        "Muhammad Fauzan Ali Fatah",
        "Firman",
        "Ahmad Naufal Dzaky",
        "Nadien Bija Manurun",
        "Husnul Nadya F",
        "Nur Hasira"
    ]
)

st.sidebar.markdown("---")

# Analisis Produksi
analisis = st.sidebar.selectbox(
    "🌾 Pilih Analisis Produksi",
    ('Jagung', 'Kedelai', 'Jagung & Kedelai')
)

# -------------------
# Tombol Download di Sidebar
st.sidebar.subheader("📥 Silahkan Download Data Disini!!")


# Data Excel
with open("data/Produksi Jagung dan Kedelai Menurut Provinsi, 2015.xlsx", "rb") as file:
    st.sidebar.download_button(
        label="⬇️ Unduh Data Excel (.xlsx)",
        data=file,
        file_name="Produksi Jagung dan Kedelai Menurut Provinsi, 2015.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Data CSV
with open("data/Produksi Jagung dan Kedelai Menurut Provinsi, 2015.csv", "rb") as file:
    st.sidebar.download_button(
        label="⬇️ Unduh Data CSV (.csv)",
        data=file,
        file_name="Produksi Jagung dan Kedelai Menurut Provinsi, 2015.csv",
        mime="text/csv"
    )


# -------------------
# Uploader di Sidebar
st.sidebar.subheader("📂 Upload File Data")
data_source = st.sidebar.radio(
    "Pilih sumber data:",
    ('XLSX', 'CSV')
)


# -------------------

#1. Halaman Utama
st.title("🌽 Analisis Produksi Jagung & Kedelai 2015")
st.subheader(f"👤 Profil Anggota: {selected_member}")

#2. Profil anggota
profil_anggota = {
    "Muhammad Fauzan Ali Fatah": {"biodata": {"NIM": "240907500027", "Jurusan": "Bisnis Digital", "Minat": "Menjadi Designer dan Developer", "Hobi": "Ngoding, Main Basket"}},
    "Firman": {"biodata": {"NIM": "240907501044", "Jurusan": "Bisnis Digital", "Minat": "Data analyst dan entrepreneur", "Hobi": "Main Volly"}},
    "Ahmad Naufal Dzaky": {"biodata": {"NIM": "240907502037", "Jurusan": "Bisnis Digital", "Minat": "Start Up Digital, Desain Kreatif & Branding", "Hobi": "Membaca, Mendengarkan Musik, & Membuat logo/desain random di Canva"}},
    "Nadien Bija Manurun": {"biodata": {"NIM": "240907500031", "Jurusan": "Bisnis Digital", "Minat": "Menanam", "Hobi": "Fotography"}},
    "Husnul Nadya F": {"biodata": {"NIM": "240907502036", "Jurusan": "Bisnis Digital", "Minat": "Menjadi Dokter Anestesi", "Hobi": "Menyanyi, Menari, Bermain Gitar, Bermain Volly"}},
    "Nur Hasira": {"biodata": {"NIM": "240907500034", "Jurusan": "Bisnis Digital", "Minat": "Menjadi Ahli Gizi", "Hobi": "Mendengarkan Musik"}}
}

data_selected = profil_anggota[selected_member]

# Tabel Biodata
biodata_df = pd.DataFrame(list(data_selected["biodata"].items()), columns=["Keterangan", "Isi"])
st.table(biodata_df)

#3. Upload Data
uploaded_file = None
if data_source == 'XLSX':
    uploaded_file = st.sidebar.file_uploader("Upload file Excel (.xlsx)", type=['xlsx'])
elif data_source == 'CSV':
    uploaded_file = st.sidebar.file_uploader("Upload file CSV (.csv)", type=['csv'])

df = None
if uploaded_file is not None:
    if data_source == 'XLSX':
        df = pd.read_excel(uploaded_file)
    elif data_source == 'CSV':
        df = pd.read_csv(uploaded_file)
    
    # Tampilkan preview data setelah upload
    st.subheader("📋 Preview Data")
    st.dataframe(df)

#4. Proses Data Jika Ada
if df is not None:
    # Bersihkan nama kolom
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'[^\w\s]', '', regex=True)
    
    if 'provinsi' not in df.columns:
        st.error("Kolom 'provinsi' tidak ditemukan di data. Mohon cek file yang diupload.")
    else:
        st.write("Kolom setelah pembersihan:", df.columns.tolist())  # debug kolom
    
        jagung_cols = [col for col in df.columns if 'produksi_jagung' in col]
        kedelai_cols = [col for col in df.columns if 'produksi_kedelai' in col]
    
        if not jagung_cols or not kedelai_cols:
            st.error("Kolom dengan 'produksi_jagung' atau 'produksi_kedelai' tidak ditemukan dalam data. Mohon cek kembali file yang diupload.")
        else:
            jagung_col = jagung_cols[0]
            kedelai_col = kedelai_cols[0]
    
            # Konversi Numerik
            df[jagung_col] = pd.to_numeric(df[jagung_col], errors='coerce')
            df[kedelai_col] = pd.to_numeric(df[kedelai_col], errors='coerce')
    
            # Info Data
            buffer = io.StringIO()
            df.info(buf=buffer)
            info_str = buffer.getvalue()
    
            st.subheader("📑 Info Data")
            st.markdown(f"```plaintext\n{info_str}\n```")
    
            # Statistik Deskriptif
            st.subheader("📊 Statistik Deskriptif")
            if analisis == 'Jagung':
                st.dataframe(df[[jagung_col]].describe())
            elif analisis == 'Kedelai':
                st.dataframe(df[[kedelai_col]].describe())
            else:
                st.dataframe(df[[jagung_col, kedelai_col]].describe())
    
            # Total Produksi
            total_jagung = df[jagung_col].sum(skipna=True)
            total_kedelai = df[kedelai_col].sum(skipna=True)
    
            col1, col2 = st.columns(2)
            col1.metric("🌽 Total Produksi Jagung Nasional", f"{total_jagung:,.0f} ton")
            col2.metric("🥜 Total Produksi Kedelai Nasional", f"{total_kedelai:,.0f} ton")
    
            # Produksi Tertinggi & Terendah
            max_jagung = df.loc[df[jagung_col].idxmax()]
            min_jagung = df.loc[df[jagung_col].idxmin()]
            max_kedelai = df.loc[df[kedelai_col].idxmax()]
            min_kedelai = df.loc[df[kedelai_col].idxmin()]
    
            st.subheader("🏆 Provinsi Produksi Tertinggi & Terendah")
            if analisis == 'Jagung':
                st.write(f"🌽 **Jagung Tertinggi**: {max_jagung['provinsi']} ({max_jagung[jagung_col]:,.0f} ton)")
                st.write(f"🌽 **Jagung Terendah**: {min_jagung['provinsi']} ({min_jagung[jagung_col]:,.0f} ton)")
            elif analisis == 'Kedelai':
                st.write(f"🥜 **Kedelai Tertinggi**: {max_kedelai['provinsi']} ({max_kedelai[kedelai_col]:,.0f} ton)")
                st.write(f"🥜 **Kedelai Terendah**: {min_kedelai['provinsi']} ({min_kedelai[kedelai_col]:,.0f} ton)")
            else:
                st.write(f"🌽 **Jagung Tertinggi**: {max_jagung['provinsi']} ({max_jagung[jagung_col]:,.0f} ton)")
                st.write(f"🌽 **Jagung Terendah**: {min_jagung['provinsi']} ({min_jagung[jagung_col]:,.0f} ton)")
                st.write(f"🥜 **Kedelai Tertinggi**: {max_kedelai['provinsi']} ({max_kedelai[kedelai_col]:,.0f} ton)")
                st.write(f"🥜 **Kedelai Terendah**: {min_kedelai['provinsi']} ({min_kedelai[kedelai_col]:,.0f} ton)")
    
            # Korelasi
            if analisis in ['Jagung', 'Kedelai']:
                st.subheader(f"🔗 Korelasi Produksi Jagung vs Kedelai")
                correlation = df[jagung_col].corr(df[kedelai_col])
                st.write(f"Korelasi: **{correlation:.2f}**")
    
            # Rasio Kedelai / Jagung
            if analisis in ['Kedelai', 'Kedua']:
                df['rasio_kedelai_jagung'] = np.where(df[jagung_col] != 0, df[kedelai_col] / df[jagung_col], np.nan)
                st.subheader("📊 Top 5 Rasio Kedelai/Jagung per Provinsi")
                st.dataframe(df[['provinsi', 'rasio_kedelai_jagung']].sort_values(by='rasio_kedelai_jagung', ascending=False).head())
    
            # Grafik Produksi
            st.subheader("📈 Grafik Produksi per Provinsi")
            if analisis == 'Jagung':
                chart_data = df[['provinsi', jagung_col]].rename(columns={jagung_col: 'Produksi'})
                chart_data['Komoditas'] = 'Jagung'
            elif analisis == 'Kedelai':
                chart_data = df[['provinsi', kedelai_col]].rename(columns={kedelai_col: 'Produksi'})
                chart_data['Komoditas'] = 'Kedelai'
            else:
                chart_data = df[['provinsi', jagung_col, kedelai_col]].melt(id_vars='provinsi', var_name='Komoditas', value_name='Produksi')
    
            bar_chart = alt.Chart(chart_data).mark_bar().encode(
                x=alt.X('provinsi:N', sort='-y', title="Provinsi"),
                y=alt.Y('Produksi:Q', title='Produksi (ton)'),
                color='Komoditas:N',
                tooltip=['provinsi:N', 'Komoditas:N', 'Produksi:Q']
            ).properties(width=800, height=400)
            st.altair_chart(bar_chart, use_container_width=True)
    
            # Pie Chart
            if analisis in ['Jagung', 'Kedelai', 'Kedua']:
                st.subheader(f"🥧 Pie Chart Kontribusi Provinsi - {analisis}")
                if analisis == 'Jagung':
                    fig = px.pie(df, names='provinsi', values=jagung_col, title='Kontribusi Produksi Jagung per Provinsi', hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
                elif analisis == 'Kedelai':
                    fig = px.pie(df, names='provinsi', values=kedelai_col, title='Kontribusi Produksi Kedelai per Provinsi', hole=0.4)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig1 = px.pie(df, names='provinsi', values=jagung_col, title='Kontribusi Produksi Jagung per Provinsi', hole=0.4)
                    fig2 = px.pie(df, names='provinsi', values=kedelai_col, title='Kontribusi Produksi Kedelai per Provinsi', hole=0.4)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(fig1, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig2, use_container_width=True)

# ---------------------
# 📌 Data Numerik  + Visualisasi
if df is not None and 'provinsi' in df.columns:
    st.subheader("📌 Data Numerik")

    jagung_col = [col for col in df.columns if 'produksi_jagung' in col][0]
    kedelai_col = [col for col in df.columns if 'produksi_kedelai' in col][0]

    num_prov = df['provinsi'].nunique()
    avg_jagung = df[jagung_col].mean()
    avg_kedelai = df[kedelai_col].mean()
    above_avg_jagung = df[df[jagung_col] > avg_jagung].shape[0]
    above_avg_kedelai = df[df[kedelai_col] > avg_kedelai].shape[0]

    st.markdown(f"""
    - 🔢 **Jumlah Provinsi**: {num_prov}
    - 🌽 **Rata-rata Produksi Jagung**: {avg_jagung:,.0f} ton
    - 🥜 **Rata-rata Produksi Kedelai**: {avg_kedelai:,.0f} ton
    - 🌽 **Provinsi dengan Produksi Jagung di atas rata-rata**: {above_avg_jagung}
    - 🥜 **Provinsi dengan Produksi Kedelai di atas rata-rata**: {above_avg_kedelai}
    """)

    # Grafik Rata-rata Produksi Jagung vs Kedelai
    st.subheader("📊 Grafik Rata-rata Produksi Jagung vs Kedelai")
    rata2_data = pd.DataFrame({
        'Komoditas': ['Jagung', 'Kedelai'],
        'Rata-rata Produksi': [avg_jagung, avg_kedelai]
    })

    fig_avg = px.bar(
        rata2_data,
        x='Komoditas',
        y='Rata-rata Produksi',
        color='Komoditas',
        text='Rata-rata Produksi',
        title='Rata-rata Produksi Jagung vs Kedelai (2015)',
        color_discrete_sequence=['#F4A300', '#A67558']
    )
    fig_avg.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_avg.update_layout(yaxis_title='Produksi (ton)', xaxis_title='Komoditas')

    st.plotly_chart(fig_avg, use_container_width=True)

    # Grafik Provinsi dengan Produksi di Atas Rata-rata
    st.subheader("📊 Jumlah Provinsi di Atas Rata-rata Produksi")
    above_avg_df = pd.DataFrame({
        'Komoditas': ['Jagung', 'Kedelai'],
        'Jumlah Provinsi': [above_avg_jagung, above_avg_kedelai]
    })

    fig_above = px.bar(
        above_avg_df,
        x='Komoditas',
        y='Jumlah Provinsi',
        color='Komoditas',
        text='Jumlah Provinsi',
        title='Provinsi dengan Produksi di Atas Rata-rata',
        color_discrete_sequence=['#F4A300', '#A67558']
    )
    fig_above.update_traces(textposition='outside')
    fig_above.update_layout(yaxis_title='Jumlah Provinsi', xaxis_title='Komoditas')

    st.plotly_chart(fig_above, use_container_width=True)

    # 🔽 Tambahan: Grafik Distribusi Provinsi Berdasarkan Kategori
    st.subheader("📊 Distribusi Provinsi Berdasarkan Kategori Produksi")

    # Tambahkan kolom kategori
    df['kategori_jagung'] = np.where(df[jagung_col] > avg_jagung, 'Di Atas Rata-rata', 'Di Bawah Rata-rata')
    df['kategori_kedelai'] = np.where(df[kedelai_col] > avg_kedelai, 'Di Atas Rata-rata', 'Di Bawah Rata-rata')

    # Hitung jumlah per kategori
    prov_jagung = df['kategori_jagung'].value_counts().reset_index()
    prov_jagung.columns = ['Kategori', 'Jumlah Provinsi']
    prov_jagung['Komoditas'] = 'Jagung'

    prov_kedelai = df['kategori_kedelai'].value_counts().reset_index()
    prov_kedelai.columns = ['Kategori', 'Jumlah Provinsi']
    prov_kedelai['Komoditas'] = 'Kedelai'

    # Gabungkan untuk visualisasi
    provinsi_kategori_df = pd.concat([prov_jagung, prov_kedelai])

    # Visualisasi
    fig_kategori = px.bar(
        provinsi_kategori_df,
        x='Komoditas',
        y='Jumlah Provinsi',
        color='Kategori',
        barmode='group',
        text='Jumlah Provinsi',
        title='Distribusi Provinsi Berdasarkan Rata-rata Produksi Jagung & Kedelai',
        color_discrete_map={
            'Di Atas Rata-rata': '#2ca02c',
            'Di Bawah Rata-rata': '#d62728'
        }
    )
    fig_kategori.update_traces(textposition='outside')
    fig_kategori.update_layout(yaxis_title='Jumlah Provinsi', xaxis_title='Komoditas')

    st.plotly_chart(fig_kategori, use_container_width=True)

if df is not None and 'provinsi' in df.columns:
    jagung_col = [col for col in df.columns if 'produksi_jagung' in col][0]
    kedelai_col = [col for col in df.columns if 'produksi_kedelai' in col][0]

    st.subheader("📊 Distribusi Produksi Jagung & Kedelai per Provinsi")

    # Ubah data jadi format long dengan provinsi tetap ada
    df_long = df.melt(id_vars='provinsi', value_vars=[jagung_col, kedelai_col], 
                      var_name='Komoditas', value_name='Produksi')

    # Boxplot dengan provinsi di tooltip
    fig_box = px.box(
        df_long,
        x='Komoditas',
        y='Produksi',
        color='Komoditas',
        title='Boxplot Produksi Jagung & Kedelai (dengan info Provinsi)',
        color_discrete_map={jagung_col: '#F4A300', kedelai_col: '#A67558'},
        hover_data=['provinsi', 'Produksi']
    )
    st.plotly_chart(fig_box, use_container_width=True)

    # Histogram (provinsi tidak ditampilkan karena bisa bikin histogram jadi terlalu ramai)
    fig_hist = px.histogram(
        df_long,
        x='Produksi',
        color='Komoditas',
        barmode='overlay',
        opacity=0.7,
        title='Histogram Distribusi Produksi Jagung & Kedelai',
        color_discrete_map={jagung_col: '#F4A300', kedelai_col: '#A67558'},
        hover_data=['provinsi']
    )
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)

# Jika ingin menganalisi satu persatu
# Analisis per provinsi
if df is not None and 'provinsi' in df.columns:
    selected_provinsi = st.selectbox("Pilih Provinsi untuk Analisis Detail", options=df['provinsi'].unique())
    df_filtered = df[df['provinsi'] == selected_provinsi]
    st.write(f"Data untuk Provinsi: {selected_provinsi}")
    st.dataframe(df_filtered)

if df is not None and 'provinsi' in df.columns:
    # ... kode daftar provinsi dan filter sebelumnya ...

    # Statistik deskriptif per provinsi
    st.subheader(f"📊 Statistik Produksi di Provinsi {selected_provinsi}")
    stats_prov = df_filtered[[jagung_col, kedelai_col]].describe()
    st.dataframe(stats_prov)

    # Grafik Produksi per Komoditas di provinsi yang dipilih
    st.subheader(f"📈 Grafik Produksi Jagung & Kedelai di Provinsi {selected_provinsi}")
    data_prov = df_filtered.melt(id_vars=['provinsi'], value_vars=[jagung_col, kedelai_col],
                                var_name='Komoditas', value_name='Produksi')
    data_prov['Komoditas'] = data_prov['Komoditas'].str.replace('produksi_', '').str.replace('_', ' ').str.title()

    fig_prov = px.bar(
        data_prov,
        x='Komoditas',
        y='Produksi',
        color='Komoditas',
        title=f"Produksi Jagung & Kedelai di {selected_provinsi} (2015)",
        text='Produksi',
        color_discrete_sequence=['#F4A300', '#A67558']
    )
    fig_prov.update_traces(textposition='outside')
    fig_prov.update_layout(yaxis_title='Produksi (ton)', xaxis_title='Komoditas')

    st.plotly_chart(fig_prov, use_container_width=True)

# Perbandingan Produksi
if df is not None and 'provinsi' in df.columns:
    # Pilih beberapa provinsi untuk perbandingan
    provinsi_list = df['provinsi'].unique().tolist()
    selected_provs = st.multiselect(
        "📍 Pilih Provinsi untuk Perbandingan Produksi (Bisa pilih lebih dari satu):",
        provinsi_list,
        default=provinsi_list[:2]
    )

    if selected_provs:
        df_compare = df[df['provinsi'].isin(selected_provs)]

# Statistik deskriptif per provinsi yang dipilih
        st.subheader("📊 Statistik Produksi Per Provinsi (Perbandingan)")
        stats_compare = df_compare.groupby('provinsi')[[jagung_col, kedelai_col]].describe()
        st.dataframe(stats_compare)

# Visualisasi perbandingan produksi jagung & kedelai per provinsi
        st.subheader("📈 Grafik Perbandingan Produksi Jagung & Kedelai")
        df_melt_compare = df_compare.melt(
            id_vars=['provinsi'], 
            value_vars=[jagung_col, kedelai_col],
            var_name='Komoditas', 
            value_name='Produksi'
        )
        df_melt_compare['Komoditas'] = df_melt_compare['Komoditas'].str.replace('produksi_', '').str.replace('_', ' ').str.title()

        fig_compare = px.bar(
            df_melt_compare,
            x='provinsi',
            y='Produksi',
            color='Komoditas',
            barmode='group',
            title="Perbandingan Produksi Jagung & Kedelai Antar Provinsi",
            text='Produksi',
            color_discrete_sequence=['#F4A300', '#A67558']
        )
        fig_compare.update_traces(textposition='outside')
        fig_compare.update_layout(xaxis_title="Provinsi", yaxis_title="Produksi (ton)")

        st.plotly_chart(fig_compare, use_container_width=True)


st.sidebar.markdown("---")