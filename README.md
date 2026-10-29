# FashionCGAN

<img src="laporan/Tel-U-Logo.png" alt="Logo Universitas Telkom" height="64" align="right">

Conditional GAN berbasis **multi-layer perceptron** murni PyTorch yang membangkitkan citra pakaian Fashion-MNIST 28×28 grayscale berdasarkan label kelas. Tidak ada model pretrained dan tidak ada implementasi GAN siap pakai — semua komponen ditulis dari dasar agar mekanisme conditioning dan loss adversarial terlihat utuh.

Tugas mata kuliah **Generative AI**, Program Studi Informatika, Universitas Telkom.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyTorch](https://img.shields.io/badge/pytorch-2.2%2B-orange)
![Tests](https://img.shields.io/badge/tests-36%20passed-brightgreen)
![Device](https://img.shields.io/badge/trained%20on-CPU-lightgrey)

## Hasil singkat

| Metrik | Nilai |
|---|---|
| Loss Discriminator (epoch 50) | 1,2613 |
| Loss Generator (epoch 50) | 0,9564 |
| Akurasi classifier pada data asli | 0,8755 |
| Akurasi gambar generator (rata-rata 10 kelas) | 0,8670 |
| Waktu training | 1.061,2 detik (50 epoch, batch 128, CPU) |
| Kelas terbaik / terlemah | Trouser 1,00 / Shirt 0,62 |

| Progres training | Sampel per kelas |
|---|---|
| ![Progres](outputs/figures/progression_by_epoch.png) | ![Sampel](outputs/figures/samples_per_class.png) |

> [!NOTE]
> Gambar di atas dihasilkan oleh `notebooks/report_visuals.ipynb` dari artefak di `outputs/figures/`. Folder `outputs/` diabaikan Git, jadi setelah clone gambar baru muncul setelah notebook dijalankan.

## Fitur

- **cGAN MLP** — Generator `[noise ⊕ one-hot]` dan Discriminator `[image ⊕ one-hot]`, tanpa lapisan konvolusi.
- **Training reproducible** — seed Python/NumPy/PyTorch, shuffle deterministik, konfigurasi YAML.
- **Resume training** — lanjutkan dari checkpoint epoch mana pun (`--resume`).
- **Evaluasi tanpa pretrained** — classifier MLP terpisah dilatih dari data asli, lalu dipakai menilai gambar generator per kelas.
- **Visualisasi siap laporan** — 8 gambar PNG + ringkasan Markdown/JSON.
- **Dokumentasi lengkap** — arsitektur, metode evaluasi, rencana implementasi, serta log dan evidence sesi AI setiap anggota.

## Struktur proyek

```text
FashionCGAN/
├── configs/default.yaml        # seed, data, model, training
├── src/fashion_cgan/
│   ├── data.py                 # Fashion-MNIST, normalisasi [-1,1], loader
│   ├── models.py               # Generator, Discriminator
│   ├── train.py                # loop cGAN + CLI
│   ├── generate.py             # grid citra per label
│   ├── evaluate.py             # classifier + akurasi per kelas
│   └── utils.py                # seed, konfigurasi, checkpoint
├── tests/                      # 36 unit test (pytest)
├── notebooks/report_visuals.ipynb
├── docs/                       # arsitektur, evaluasi, rencana, log AI
├── evidence/                   # transkrip sesi AI tiap anggota
├── tools/                      # build_report.py, pptx_build/, pembersih evidence
└── laporan/                    # LaTeX + PDF laporan + PPTX presentasi
```

## Prasyarat

- Python 3.10 atau lebih baru
- ±2 GB ruang disk untuk dataset, checkpoint, dan artefak
- CPU sudah cukup; GPU opsional

## Mulai cepat

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

python -m pip install -r requirements.txt
```

Uji cepat apakah pipeline berjalan (1 epoch, 20 batch):

```bash
set PYTHONPATH=src                       # PowerShell: $env:PYTHONPATH="src"
python -m fashion_cgan.train --epochs 1 --max-batches 20
```

## Training

```bash
python -m fashion_cgan.train --config configs/default.yaml
```

Pengaturan bawaan di [`configs/default.yaml`](configs/default.yaml):

| Parameter | Nilai |
|---|---|
| Seed | 42 (`random`, NumPy, PyTorch, shuffle) |
| Latent dim | 100 |
| Optimizer | Adam, lr `2e-4`, betas `(0.5, 0.999)` |
| Loss | `BCEWithLogitsLoss` |
| Batch size / epoch | 128 / 50 |
| Normalisasi | `[-1, 1]` |

Opsi CLI yang tersedia:

```text
--config PATH          berkas konfigurasi (default: configs/default.yaml)
--epochs N             menimpa jumlah epoch
--max-batches N        batasi batch per epoch (smoke test)
--download/--no-download  unduh Fashion-MNIST bila belum ada
--resume PATH          lanjutkan dari checkpoint
--device DEVICE        cpu / cuda
```

Setiap epoch menulis `outputs/cgan_epoch_N.pt` dan satu baris ke `outputs/metrics.csv`.

## Membangkitkan gambar

```bash
python -m fashion_cgan.generate outputs/cgan_epoch_50.pt \
    --labels 0 1 2 --output outputs/grid.png
```

Tanpa `--labels`, satu sampel untuk kesepuluh kelas dibuat.

## Evaluasi

```bash
python -m fashion_cgan.evaluate outputs/cgan_epoch_50.pt \
    --output-dir outputs/evaluation \
    --epochs 5 \
    --samples-per-class 100
```

Classifier MLP dilatih hanya dari data asli (tanpa pretrained), lalu 100 gambar per kelas diuji. Hasil ditulis ke `evaluation.json` dan `evaluation.csv`.

| Kelas | Akurasi generator |
|---|---|
| T-shirt/top | 0,94 |
| Trouser | 1,00 |
| Pullover | 0,84 |
| Dress | 0,89 |
| Coat | 0,75 |
| Sandal | 0,99 |
| Shirt | 0,62 |
| Sneaker | 0,88 |
| Bag | 0,93 |
| Ankle boot | 0,83 |

Metode dan batasannya dijelaskan di [`docs/evaluation.md`](docs/evaluation.md).

## Pengujian

```bash
# Windows PowerShell
$env:PYTHONPATH="src"; python -m pytest tests -q

# Linux / macOS
PYTHONPATH=src python -m pytest tests -q
```

Hasil saat ini: **36 passed** (data, model, training, resume, generate, evaluate, utils).

## Notebook laporan

[`notebooks/report_visuals.ipynb`](notebooks/report_visuals.ipynb) hanya membaca artefak `outputs/` — tanpa training — dan menghasilkan 8 gambar ke `outputs/figures/` beserta `summary.md` dan `summary.json`:

| Gambar | Isi |
|---|---|
| `dataset_samples.png` | Satu citra asli per kelas |
| `class_distribution.png` | Distribusi 60.000 citra latih |
| `loss_curve.png` | Loss D dan G per epoch |
| `progression_by_epoch.png` | Keluaran epoch 1, 25, 50 dengan noise tetap |
| `samples_per_class.png` | Empat sampel generator per kelas |
| `grid_one_per_class.png` | Satu sampel per kelas |
| `diversity_per_class.png` | Dua belas sampel pada empat kelas |
| `classifier_accuracy.png` | Akurasi asli vs generator per kelas |

## Dokumen dan presentasi

| Berkas | Isi |
|---|---|
| `laporan/Laporan-tugas-generative-ai-...-fashion-mnist.pdf` | Laporan akhir (LaTeX, 32 halaman, margin sesuai template) |
| `laporan/Presentasi-FashionCGAN-Conditional-GAN-MLP.pptx` | Deck 14 slide + speaker notes |
| [`laporan/README.md`](laporan/README.md) | Struktur LaTeX dan cara kompilasi |
| [`tools/pptx_build/README.md`](tools/pptx_build/README.md) | Cara meregenerasi deck |

```bash
python tools/build_report.py      # pdfLaTeX + BibTeX, PDF dinamai sesuai judul
cd tools/pptx_build && node build_deck.js   # butuh npm install sekali
```

## Dokumentasi

- [`docs/architecture.md`](docs/architecture.md) — kontrak tensor dan bentuk lapisan
- [`docs/evaluation.md`](docs/evaluation.md) — classifier, metrik, dan interpretasi
- [`docs/implementation-plan.md`](docs/implementation-plan.md) — urutan kerja dan pembagian anggota
- [`docs/ai-logs/README.md`](docs/ai-logs/README.md) — aturan pencatatan sesi AI

Kontrak rancangan:

| Objek | Bentuk / rentang |
|---|---|
| Gambar dataset | `[B, 1, 28, 28]`, float `[-1, 1]` |
| Label | `[B]`, integer `0..9`, di-encode one-hot |
| Input Generator | noise `[B, 100]` + one-hot `[B, 10]` |
| Keluaran Generator | `[B, 1, 28, 28]` via `Tanh` |
| Keluaran Discriminator | `[B]` logit, tanpa sigmoid |

## Log AI dan evidence

Setiap anggota mencatat sesi AI memakai format yang sama. Salin [`docs/ai-logs/session-template.md`](docs/ai-logs/session-template.md), simpan bukti asli di `evidence/<nama-anggota>/`, dan jangan pernah menulis log atau hasil pengujian fiktif — hanya kejadian yang benar-benar terjadi.

## Tim

| Anggota | NIM | Peran |
|---|---|---|
| Ivander Dzaky Khairullah | 103012300174 | Prompt Engineer & Model Architect — model, unit test |
| Muhammad Ragil | 103012300015 | Data Pipeline & Training Engineer — dataset, training, eksperimen |
| Silmi Sila Nia Uma | 103012430070 | Documentation & Evaluation Engineer — evaluasi, visualisasi, dokumentasi |

Dosen pengampu: Dr. Aditya Firman Ihsan, S.Si., M.Si.

## Catatan

Dataset, checkpoint, dan artefak besar tidak masuk Git (lihat `.gitignore`). Jalankan training atau notebook sekali agar folder `data/` dan `outputs/` terisi.
