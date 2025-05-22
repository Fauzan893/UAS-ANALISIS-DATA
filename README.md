# Proses Analisis

A. Cara Analisis Data
1. Membuat folder enviroment agar bisa melakukan analisis menggunakan streamlit dengan cara python -m venv env jalankan di terminal
2. Mengaktifkan enviroment dengan cara source env/bin/activate (untuk linux) atau env\Scripts\activate (untuk windows)
3. Setelah kami mencari sebuah dataset.
4. Kami melakukan analisis dengan menggunakan bahasa python, menggunakan library pandas dan matplotlib agar menghasilkan grafik.
5. Kami melakukan install atau import sebuah library pandas dengan cara pip install pandas
6. Kami melakukan install atau import sebuah library numpy dengan cara pip install numpy
7. Kamu juga melakukan install atau import  matplotlib dengan cara pip install matplotlib untuk tampilan sebuah grafik


# Penjelasan Pada Web
1. Judul dan Tujuan Aplikasi
Judul: Analisis Produksi Jagung & Kedelai 2015
Tujuan: Memudahkan analisis data produksi jagung dan kedelai per provinsi di Indonesia tahun 2015 dengan manipulasi data dan numerik untuk melihat statistik, grafik, dan unduh data.

2. Fitur Sidebar
Informasi Kelompok: Menampilkan data mata kuliah dan anggota kelompok.
Pemilihan Anggota Kelompok: Pilih anggota untuk menampilkan biodata lengkapnya.
Pemilihan Jenis Analisis: Disini kami menggunakan jenis analisis agar mempermudah pengguna untuk melihat data yang di analisis dan data yang ditampilkan itu sesuai yang pengguna mau lihat misalnya dia ingin melihat analisis tentang jagung saja atau kedelai ataupun keduanya.
Download Data: Disini kami menyediakan fitur download data agar pengguna dapat mengunduh data yang telah di analisis.
Upload Data: Pengguna dapat mengunggah file data yang telah disediakan agar bisa hasil analisis, apabila menggunakan data lain maka web tersebut tidak dapat di analisis dengan sempurna.

3. Profil Anggota Kelompok
Disini kami menampilkan nama kelompok agar bisa dilihat oleh semua orang

4. Data Preview
Setelah upload data, aplikasi otomatis menampilkan preview data. Anda juga dapat memastikan kolom penting seperti provinsi, produksi_jagung, dan produksi_kedelai yang telah dianalisis.

5. Analisis Data Produksi
Statistik Deskriptif: Menampilkan ringkasan statistik seperti rata-rata, maksimum, minimum produksi jagung dan kedelai.
Total Produksi Nasional: Menampilkan total produksi jagung dan kedelai secara nasional.
Provinsi Produksi Tertinggi dan Terendah: Mengidentifikasi provinsi dengan produksi tertinggi dan terendah untuk masing-masing komoditas.
Korelasi Produksi Jagung dan Kedelai: Menghitung dan menampilkan nilai korelasi antara produksi jagung dan kedelai.
Rasio Produksi Kedelai terhadap Jagung: Menampilkan provinsi dengan rasio tertinggi antara produksi kedelai dan jagung.

6. Visualisasi Data
Bar Chart: Grafik batang yang menunjukkan produksi jagung dan kedelai per provinsi.
Pie Chart: Diagram lingkaran untuk melihat kontribusi produksi tiap provinsi.
Grafik Rata-Rata Produksi: Perbandingan rata-rata produksi jagung dan kedelai secara nasional.
Grafik Jumlah Provinsi di Atas Rata-Rata: Menunjukkan berapa provinsi yang produksi jagung dan kedelainya di atas rata-rata.
Distribusi Kategori Produksi: Grafik distribusi provinsi berdasarkan apakah produksi mereka di atas atau di bawah rata-rata.
Boxplot & Histogram: Visualisasi distribusi produksi dan penyebarannya.

7. Analisis Per Provinsi
Pengguna dapat memilih provinsi tertentu untuk melihat data detail, statistik, dan grafik produksi jagung dan kedelai di provinsi tersebut.

8. Bahasa yang di gunakan pada sebuah analisis data
Python dengan Streamlit: Membuat aplikasi web interaktif dengan mudah.
Pandas dan NumPy: Untuk manipulasi dan analisis data.
Altair dan Plotly: Untuk visualisasi data interaktif yang menarik.
