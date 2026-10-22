# Rencana Implementasi dan Kontribusi

## Pembagian kerja

| Anggota | Area utama | Berkas yang direncanakan |
|---|---|---|
| 1 — Ivander Dzaky Khairullah — Prompt Engineer & Model Architect | Rancangan, Generator/Discriminator, uji model | `src/fashion_cgan/models.py`, `tests/test_models.py`, `docs/architecture.md` |
| 2 — Muhammad Ragil — Data Pipeline & Training Engineer | Dataset, DataLoader, training loop, eksperimen | `src/fashion_cgan/data.py`, `src/fashion_cgan/train.py`, `configs/default.yaml`, `tests/test_data.py` |
| 3 — Silmi Sila Nia Uma — Documentation & Evaluation Engineer | Evaluasi, visualisasi, dokumentasi, laporan | `src/fashion_cgan/evaluate.py`, `src/fashion_cgan/utils.py`, `docs/`, `README.md`, `evidence/silmi-sila-nia-uma/` |

## Aturan kolaborasi

1. Setiap anggota mengubah area utama yang ditetapkan; perubahan lintas area dibicarakan sebelum dikerjakan.
2. Kontrak di `architecture.md` menjadi antarmuka bersama. Usulkan perubahan kontrak dan minta persetujuan tim sebelum mengubahnya.
3. Anggota 1 menyelesaikan model dan tes kontrak sebelum Anggota 2 mengintegrasikan training. Training tidak dimulai sampai model dan pipeline data lulus pemeriksaan.
4. Anggota 2 memiliki konfigurasi eksperimen; koordinasikan perubahan konfigurasi dengan anggota lain agar tidak ada konflik.
5. Anggota 3 mengelola dokumentasi umum; pemilik modul tetap menulis log interaksi dan perubahan untuk pekerjaannya sendiri.
6. Gunakan branch/PR per pekerjaan bila alur tim mendukungnya; hindari mengedit file yang sedang dikerjakan anggota lain.
7. Jangan commit/push tanpa persetujuan pemilik proyek. Jangan memasukkan dataset, checkpoint, rahasia, atau bukti percakapan yang berisi kredensial.

## Urutan implementasi dan gerbang

1. Sepakati kontrak model dan konfigurasi.
2. Anggota 1 implementasikan MLP cGAN; jalankan tes bentuk, conditioning, dan gradient flow.
3. Anggota 2 siapkan preprocessing `[-1,1]` dan DataLoader; jalankan tes kontrak data.
4. Tinjau integrasi model/data; uji satu batch tanpa training panjang.
5. Setelah gerbang lolos, jalankan eksperimen Colab dengan seed dan konfigurasi tercatat.
6. Anggota 3 evaluasi hasil, visualisasikan sampel tiap kelas, dokumentasikan bukti dan laporan.

## Struktur target

```text
src/fashion_cgan/   package Python
configs/            konfigurasi eksperimen
tests/              tes kontrak dan regresi
notebooks/          notebook Colab tipis untuk eksperimen
docs/               arsitektur, rencana, panduan, template log
evidence/           bukti asli per anggota
outputs/            artefak lokal yang tidak di-commit
```
