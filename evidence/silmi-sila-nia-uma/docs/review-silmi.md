# Review Tugas Besar Generative AI: FashionCGAN

**Reviewer:** Silmi Sila Nia Uma (103012430070)
**Tanggal review:** 29 Oktober 2026
**Yang direview:** laporan (PDF), slide presentasi (PPTX), dan repositori kode

## 1. Ringkasan

Proyek mengimplementasikan conditional GAN (cGAN) berbasis MLP pada Fashion-MNIST dari komponen dasar PyTorch, tanpa model pretrained. Hasilnya dievaluasi dengan classifier MLP yang dilatih dari data asli. Pipeline data, training, pembangkitan gambar, dan evaluasi sudah lengkap. Konfigurasi dan seed (42) tercatat sehingga hasil bisa direproduksi. Secara umum laporan, slide, dan README konsisten dan mudah diikuti. Catatan dan saran ada di bagian 4.

## 2. Hasil pengecekan

### 2.1 Pengujian otomatis (pytest)

- Perintah: `PYTHONPATH=src python -m pytest tests -q`
- Lingkungan: Google Colab, Python 3.13
- Hasil: **36 passed, 0 failed** (3,37 detik)
- Laporan menyebut 36 tes lulus. **Status: SESUAI.**

### 2.2 Kecocokan angka dengan isi repositori

Angka utama saya cocokkan dengan README dan dokumen di repositori.

| Besaran | Nilai | Status |
|---|---|---|
| Akurasi classifier pada data asli | 0,8755 | Cocok |
| Rata-rata akurasi generator (10 kelas) | 0,8670 | Cocok |
| Selisih akurasi asli vs generator | 0,0085 | Cocok |
| Loss Discriminator epoch 50 | 1,2613 | Cocok |
| Loss Generator epoch 50 | 0,9564 | Cocok |
| Durasi training 50 epoch | 1061,2 detik (±17,7 menit) | Cocok |
| Akurasi kelas Shirt (terendah) | 0,62 | Cocok |
| Akurasi kelas Trouser (tertinggi) | 1,00 | Cocok |

Batasan pengecekan ini: folder `outputs/` (checkpoint dan `metrics.csv`) tidak ikut repositori karena dikecualikan `.gitignore`. Jadi saya memeriksa **konsistensi antar dokumen**, belum menghitung ulang dari hasil mentah. Verifikasi penuh memerlukan checkpoint epoch 50 dari anggota yang melakukan training.

### 2.3 Kode evaluasi

- `src/fashion_cgan/evaluate.py` (190 baris): `Classifier` (MLP kecil dari nol), `train_classifier`, `classifier_accuracy`, `generated_class_accuracy`, `evaluate`, dan `main`. Alur: latih classifier di data asli, ukur akurasi di test split asli sebagai batas atas, lalu ukur kecocokan gambar generator dengan label yang diminta.
- `src/fashion_cgan/utils.py` (70 baris): `denormalize` (dari [-1, 1] ke [0, 1]), `load_metrics` (baca CSV metrik), `save_image_grid` (simpan grid PNG), `class_names`.
- Fungsi sudah bernama jelas dan hampir semua punya docstring. Hanya `main` di `evaluate.py` yang belum.

### 2.4 Kerapian dokumentasi

Berkas dan folder utama (`README.md`, `AGENTS.md`, `requirements.txt`, `configs/default.yaml`, `docs`, `notebooks`, `evidence`, `tests`) semuanya ada. Tidak ada penanda "belum selesai" di berkas `.md`, dan tidak ada berkas `.md` yang kosong atau terlalu pendek.

## 3. Analisis hasil evaluasi

- **Kecocokan label baik secara keseluruhan.** Rata-rata akurasi generator 0,8670 hanya terpaut 0,0085 dari akurasi classifier pada data asli (0,8755). Artinya generator umumnya menghasilkan gambar yang dikenali sesuai kelas yang diminta, jadi mekanisme conditioning bekerja.
- **Kelas terbaik:** Trouser (1,00) dan Sandal (0,99). Bentuk kedua kelas ini khas dan jarang tertukar dengan kelas lain.
- **Kelas terlemah:** Shirt (0,62), lalu Coat (0,75), Ankle boot (0,83), dan Pullover (0,84). Dugaan saya, Shirt tertukar dengan T-shirt, Pullover, dan Coat yang bentuknya mirip. Ini hipotesis, belum diuji. Matriks kebingungan (confusion matrix) dapat memastikannya.
- **Arti angka ini terbatas.** Metrik ini hanya mengukur "dikenali sebagai kelas yang benar", bukan kualitas visual atau keragaman gambar. Hal ini sudah diakui di `docs/evaluation.md` bagian Batasan.

## 4. Catatan dan saran

1. **Tambah ukuran keragaman.** Seed noise tetap per kelas, sehingga mode collapse tidak terdeteksi. Saran: hitung rata-rata jarak antar gambar dalam satu kelas, atau tambahkan FID.
2. **Tambah confusion matrix** pada gambar generator untuk menjelaskan kenapa Shirt rendah, sehingga analisis tidak berhenti pada angka.
3. **Ulangi classifier dengan beberapa seed** dan laporkan rata-rata serta sebarannya. Classifier kecil dan dilatih singkat (5 epoch), sehingga angka 0,8755 bisa berubah antar run.
4. **Sertakan checkpoint atau hasil mentah** (`metrics.csv`) di lampiran laporan atau tautan terpisah, agar angka bisa diverifikasi ulang tanpa training ulang.


## 5. Kesimpulan

Proyek siap digunakan: tes lulus (36/36), angka konsisten antar dokumen, struktur repositori rapi, dan hasil bisa direproduksi lewat seed dan konfigurasi yang tercatat. Kelemahan utama ada di cakupan evaluasi (hanya satu metrik, tanpa keragaman), bukan di kebenaran implementasi.
