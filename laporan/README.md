# Laporan LaTeX — FashionCGAN

Laporan memakai template resmi (`Template _Penulisan_Latex`) tanpa mengubah margin: kiri 4 cm, kanan/atas/bawah 3 cm (lebar teks 16 cm).

## Struktur

| Berkas | Isi |
|---|---|
| `main.tex` | Preamble template + data penulis + urutan bab |
| `Cover.tex` | Halaman judul: judul, anggota + NIM, dosen pengampu (satu halaman) |
| `Abstrak-Indo.tex` | Abstrak + kata kunci |
| `Pendahuluan.tex` | Bab I — latar belakang, rumusan, tujuan, hipotesis, rencana, jadwal |
| `Kajian-Pustaka.tex` | Bab II — GAN, cGAN, MLP, Fashion-MNIST, loss, evaluasi, penelitian terdahulu |
| `Metodologi.tex` | Bab III — alur sistem, kontrak data, arsitektur, algoritma, konfigurasi, evaluasi |
| `Hasil-Pembahasan.tex` | Bab IV — dataset, loss, progres, sampel, keragaman, akurasi, pembahasan |
| `Kesimpulan.tex` | Bab V — kesimpulan, keterbatasan, saran |
| `Lampiran.tex` | Struktur repo, perintah reproduksi, bukti sesi |
| `Laporan.md` | Versi Markdown laporan (ringkas, gaya README: teori, teknis, hasil, jobdesk) |
| `References.bib` | 11 referensi, semuanya disitasi |
| `main.bbl` | Hasil BibTeX (disertakan agar Overleaf langsung benar) |
| `Laporan-...pdf` | Hasil kompilasi; nama berkas mengikuti judul laporan |
| `*.png` | Gambar dari `outputs/figures/` + logo |

## Kompilasi lokal (MiKTeX, sudah terpasang)

```powershell
python tools/build_report.py
```

Skrip menjalankan pdfLaTeX + BibTeX + pdfLaTeX dua kali, lalu menyalin hasilnya menjadi nama PDF sesuai judul. Perintah manual:

```powershell
cd laporan
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

## Kompilasi di Overleaf

Upload seluruh isi folder `laporan/` (termasuk PNG dan `main.bbl`), atur `main.tex` sebagai dokumen utama, compiler pdfLaTeX.

## Verifikasi tata letak

- `python tools/check_report_layout.py` — cek lebar tabel ≤ 15,9 cm dan semua gambar ada.
- Pemeriksaan PDF via PyMuPDF: **0 pelanggaran margin** (kiri 4 cm, kanan/atas/bawah 3 cm) pada seluruh halaman.
- Overfull box sisa hanya antarhuruf di dalam sel (≤ 12 pt), tidak menggeser tabel keluar margin.

## Presentasi

`Presentasi-FashionCGAN-Conditional-GAN-MLP.pptx` — 14 slide 16:9 + speaker notes. Dibangun dengan `node build_deck.js` dari `tools/pptx_build/`; detail ada di README folder tersebut.

## Catatan penyesuaian

- `\usepackage[htt]{hyphenat}` ditambahkan agar path berkas panjang dapat dipotong; `\emergencystretch` dinaikkan.
- Nomor halaman footer dinaikkan (`\raisebox{0.5cm}`) agar berada di dalam batas bawah 3 cm, termasuk gaya `plain`.
- Semua tabel memakai kolom `L{...}` (paragraf rata kiri); tidak ada `tabular` dengan kolom `c` tak berlebar.
