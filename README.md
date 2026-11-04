# E-Commerce Public Data Dashboard

Dashboard **Streamlit** interaktif untuk menyajikan hasil analisis data e-commerce:

1. **Waktu Pengiriman vs Kepuasan Pelanggan** — menampilkan 10 kategori produk dengan waktu pengiriman terlama, dilengkapi review score dan jumlah pesanan.
2. **Segmentasi Pelanggan (RFM)** — analisis Recency, Frequency, Monetary yang membagi pelanggan ke dalam 4 segmen: Low, Mid, High, dan VIP.

Dokumen ini menjelaskan cara menjalankan dashboard dari nol, mulai dari pembuatan virtual environment hingga perintah `streamlit run`.

---

## Struktur Proyek

```
Dashboard/
├── dashboard.py      # Aplikasi Streamlit (kode utama)
├── main_data.csv     # Data utama (order_purchase_timestamp, product_category_name, delivery_days, review_score)
├── rfm_data.csv      # Data RFM (customer_unique_id, Recency, Frequency, Monetary, Segment)
├── requirements.txt  # Daftar dependensi Python
└── README.md         # Panduan ini
```

---

## Prasyarat

Sebelum memulai, pastikan sudah tersedia:

- **Python 3.12** (atau versi kompatibel). Cek dengan:
  ```bash
  python --version
  ```
- **pip** (biasanya sudah terpasang bersama Python). Cek dengan:
  ```bash
  pip --version
  ```

> Jika `python` tidak dikenali di macOS/Linux, gunakan `python3` dan `pip3` pada semua perintah di bawah.

---

## Cara Menjalankan Dashboard dari Awal

### 1. Buka direktori proyek

Masuk ke folder proyek `Dashboard` terlebih dahulu. Semua perintah berikut dijalankan dari dalam folder ini agar file CSV dapat ditemukan.

```bash
cd Dashboard
```

### 2. Buat virtual environment

Virtual environment memisahkan dependensi proyek dari instalasi Python global.

```bash
python -m venv venv
```

Perintah ini akan membuat folder baru bernama `venv` di dalam proyek.

### 3. Aktifkan virtual environment

Pilih perintah sesuai sistem operasi dan terminal yang digunakan:

**Windows — Command Prompt (CMD):**
```bash
venv\Scripts\activate
```

**Windows — PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux (bash/zsh):**
```bash
source venv/bin/activate
```

Jika berhasil, nama environment `(venv)` akan muncul di awal baris terminal.

> **Catatan PowerShell:** Jika muncul error *"running scripts is disabled"*, jalankan sekali perintah berikut lalu coba aktifkan kembali:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```

### 4. Instal dependensi

Setelah virtual environment aktif, instal seluruh dependensi yang tercatat di `requirements.txt`:

```bash
pip install -r requirements.txt
```

Proses ini akan mengunduh dan memasang `streamlit`, `pandas`, `numpy`, dan `plotly`.

### 5. Jalankan dashboard

Setelah instalasi selesai, jalankan aplikasi:

```bash
streamlit run dashboard.py
```

Streamlit akan menampilkan alamat di terminal dan otomatis membuka browser:

- **Local URL:** `http://localhost:8501`
- **Network URL:** `http://<IP-lokal>:8501`

Jika browser tidak terbuka otomatis, buka `http://localhost:8501` secara manual.

### 6. Hentikan dashboard

Kembali ke terminal lalu tekan **Ctrl + C** untuk menghentikan server.

### 7. (Opsional) Menonaktifkan virtual environment

Setelah selesai bekerja, keluar dari virtual environment dengan:

```bash
deactivate
```

---

## Ringkasan Perintah

Untuk pengguna Windows (CMD), seluruh langkah secara berurutan:

```bash
cd Dashboard
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run dashboard.py
```

---

## Fitur

- Filter sidebar yang fleksibel: rentang tanggal (Start/End Date), tahun, kategori produk, dan segmen RFM — semuanya menggunakan **multiselect dengan opsi "All"** agar data bisa dibandingkan lintas kondisi sekaligus.
- Slider **Top N** untuk mengatur jumlah kategori yang ditampilkan.
- Penanganan error pada filter tanggal: dashboard tetap berjalan dan menampilkan peringatan bila Start/End Date belum diisi atau rentangnya tidak valid.
- Visualisasi interaktif berbasis **Plotly** (zoom, hover detail, seleksi data) dengan palet warna seragam: satu warna netral + satu warna sorotan untuk nilai ekstrem.
- Insight callout pada setiap bagian analisis.

---

## Troubleshooting

| Masalah | Penyebab | Solusi |
| --- | --- | --- |
| `FileNotFoundError: main_data.csv` | Aplikasi dijalankan bukan dari direktori proyek | Jalankan `streamlit run dashboard.py` dari dalam folder `Dashboard` |
| `ModuleNotFoundError: No module named 'streamlit'` | Dependensi belum terpasang, atau virtual environment belum aktif | Aktifkan venv (langkah 3) lalu jalankan `pip install -r requirements.txt` |
| `Port 8501 is already in use` | Port 8501 sedang dipakai proses lain | Hentikan proses tersebut, atau jalankan dengan port lain: `streamlit run dashboard.py --server.port 8502` |
| `python is not recognized` (Windows) | Python belum ditambahkan ke PATH | Pasang ulang Python dengan opsi *"Add Python to PATH"*, atau gunakan path lengkap ke `python.exe` |
