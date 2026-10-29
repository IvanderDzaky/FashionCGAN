# Presentasi FashionCGAN (PPTX)

Deck 14 slide untuk presentasi laporan, ditulis sebagai skrip `pptxgenjs` agar bisa diregenerasi setelah data eksperimen berubah.

## Isi slide

| # | Slide | Sumber data |
|---|---|---|
| 1 | Judul + anggota + dosen | `laporan/Cover.tex` |
| 2 | Agenda | — |
| 3 | Latar belakang & tujuan | `laporan/Pendahuluan.tex` |
| 4 | Dataset Fashion-MNIST | `outputs/figures/dataset_samples.png` |
| 5 | Arsitektur Generator & Discriminator | `laporan/Metodologi.tex` |
| 6 | Prosedur pelatihan & konfigurasi | `configs/default.yaml` |
| 7 | Kurva loss D vs G | `outputs/metrics.csv` |
| 8 | Progres per epoch | `outputs/figures/progression_by_epoch.png` |
| 9 | Sampel per kelas | `outputs/figures/samples_per_class.png` |
| 10 | Keragaman | `outputs/figures/diversity_per_class.png` |
| 11 | Akurasi classifier | `outputs/evaluation.json` + `outputs/figures/classifier_accuracy.png` |
| 12 | Kesimpulan | `laporan/Kesimpulan.tex` |
| 13 | Pengembangan | `laporan/Kesimpulan.tex` |
| 14 | Penutup | — |

Speaker notes diisi di 11 slide.

## Membangun ulang

```powershell
cd tools/pptx_build
npm install      # sekali saja
node build_deck.js
```

Hasil: `laporan/Presentasi-FashionCGAN-Conditional-GAN-MLP.pptx`.

Gambar dibaca dari `outputs/figures/`, jadi jalankan notebook `notebooks/report_visuals.ipynb` lebih dulu bila folder itu kosong. Angka loss pada grafik slide 7 diambil dari `outputs/metrics.csv`; jika training diulang, perbarui larik `D` dan `G` di `build_deck.js`.

## Verifikasi

```powershell
python "$HOME/.agents/skills/pptx/scripts/office/validate.py" laporan/Presentasi-FashionCGAN-Conditional-GAN-MLP.pptx
```

Hasil terakhir: *All validations PASSED*.
