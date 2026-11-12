# Realistic Vectorized Backtesting & Volatility-Targeting Engine

Sebuah mesin penguji strategi trading kuantitatif (*backtester*) berbasis **vektorisasi penuh (Pandas & NumPy)** yang dirancang dengan standar institusional: tanpa perulangan (`for loop`) yang lambat, bebas dari bias masa depan (*zero lookahead bias*), dan dilengkapi dengan alokasi modal adaptif berbasis risiko (*dynamic volatility targeting*).

---

## 1. Apa Sih Sebenarnya Ini?

Kebanyakan pemula membuat *backtest* yang menghasilkan grafik keuntungan luar biasa di atas kertas, tetapi langsung hancur ketika dijalankan di pasar nyata (*live trading*). Hal itu biasanya terjadi karena dua dosa besar:
1. **Mengintip Masa Depan (*Lookahead Bias*):** Sistem pura-pura beli di harga penutupan hari ini, padahal harga penutupan itu baru diketahui saat candle sudah selesai.
2. **Ukuran Posisi Kaku (*Fixed Sizing*):** Membeli dengan jumlah lot atau uang yang sama, baik saat pasar sedang tenang maupun saat pasar sedang badai krisis.

**Proyek ini adalah solusi untuk kedua masalah tersebut.** 

Mesin ini memperlakukan data deret waktu seperti kondisi di lantai bursa nyata:
* Keputusan yang terkonfirmasi kemarin sore **baru sah dieksekusi pada pembukaan esok harinya**.
* Alokasi modal tidak statis, melainkan **bergerak dinamis seperti knop volume**: saat pasar bergejolak liar, sistem otomatis memangkas eksposur modal untuk melindungi portofolio; saat pasar tenang, sistem memperbesar alokasi untuk mengoptimalkan imbal hasil.
* Seluruh logika dijalankan serentak menggunakan operasi array matematika tingkat tinggi tanpa perulangan baris-demi-baris.

---

## 2. Tujuan Proyek

Proyek ini dibangun dengan fokus pada 4 tujuan utama:

### A. Menerapkan *Anti-Lookahead Hygiene* Tingkat Ketat
* Memastikan tidak ada kebocoran data (*data leakage*) pada indikator teknikal dengan menerapkan jendela observasi `closed='left'`.
* Menerapkan jeda eksekusi mutlak menggunakan `.shift(1)` agar kalkulasi return hanya terjadi setelah pesanan realistis masuk ke pasar.

### B. Membangun Engine *Volatility-Targeting* Institusional
* Mengukur *realized volatility* dinamis dari *log return* aset yang di-annualisasi ($\times \sqrt{252}$).
* Menghitung rasio bobot risiko dinamis: $\text{Bobot} = \frac{\text{Target Volatilitas}}{\text{Volatilitas Aktual}}$.
* Menerapkan *boundary masking* (`.clip()`) untuk membatasi risiko agar leverage tidak meledak di pasar yang tidur.

### C. Mereplikasi *State Machine (Hold Position)* Secara Vektorisasi
* Memecahkan masalah klasik trading: bagaimana menahan posisi (*HOLD*) selama berminggu-minggu tanpa menggunakan percabangan `if-else` atau `for loop`.
* Memanfaatkan kombinasi `np.where` bersarang (*nested*) dan perambatan status `.ffill()` untuk mengalirkan status kepemilikan aset secara instan.

### D. Menghasilkan Simulasi Kurva Modal (*Equity Curve*) yang Bersih
* Mencegah kesalahan dimensi (*broadcasting explosion*) dengan standarisasi data 1D murni (`.iloc[:, 0]`).
* Menghasilkan pelacakan pertumbuhan modal kumulatif berbasis eksponensial log return secara matematis.

---

## 3. Alur Arsitektur Sistem

```
[ 1. Data OHLCV ] 
       │
       ▼ (Kunci 1D via .iloc[:, 0])
[ 2. Log Return ] ──► [ 3. Realized Volatility (x √252) ] ──► [ 4. Bobot Dinamis (.clip) ]
       │                                                                  │
       ▼                                                                  │
[ 5. Sinyal Anomali (closed='left') ]                                     │
       │                                                                  │
       ▼                                                                  │
[ 6. Vectorized State Machine (np.where + .ffill()) ]                     │
       │                                                                  │
       ▼                                                                  │
[ 7. Anti-Lookahead Execution (.shift(1)) ]                               │
       │                                                                  │
       └───────────────────────────────┬──────────────────────────────────┘
                                       ▼
                       [ 8. Posisi Portofolio Final ]
                                       │
                                       ▼
                       [ 9. Return Strategi Kumulatif ]
                                       │
                                       ▼
                       [ 10. Visualisasi Equity Curve ]
```

---

## 4. Struktur File Terkait

* **File Skrip Utama:** `RealisticVectorizedBacktesting&Volatility-TargetingEngine.py`
* **Panduan Mental & Intuisi:** `Vectorized_Quant_Mental_Model.md` (Tersedia juga di Obsidian Vault)
* **Pondasi Latihan:** `pandaslearn.ipynb` dan `numpylearn.ipynb`

---

## 5. Ringkasan Prinsip Kerja

> *"Sinyal teknikal hanya menentukan arah (kapan masuk dan keluar), sedangkan volatilitas pasar menentukan porsi (seberapa banyak uang yang aman dipertaruhkan)."*
