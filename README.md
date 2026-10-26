# FashionCGAN

Proyek akademik untuk membangun conditional GAN (cGAN) MLP dari komponen dasar PyTorch, menghasilkan citra Fashion-MNIST grayscale 28×28 berdasarkan 10 kelas. Model pretrained dan implementasi GAN siap pakai tidak digunakan.

## Status

Generator dan Discriminator MLP conditional, preprocessing Fashion-MNIST, training cGAN, serta generate image grid sudah diimplementasikan beserta unit test. Evaluasi belum diimplementasikan.

## Persiapan lingkungan

```bash
python -m venv .venv
python -m pip install -r requirements.txt
```

Di Google Colab, pasang dependency dari `requirements.txt` bila environment belum memilikinya. Pengaturan awal ada di `configs/default.yaml`.

## Kontrak rancangan

- Dataset: gambar `[B, 1, 28, 28]` float dalam `[-1, 1]`; label integer `[B]` dalam `0..9`.
- Generator: noise `[B, 100]` dan label; gambar keluaran `[B, 1, 28, 28]` dengan `Tanh`.
- Discriminator: gambar dan label; satu logit per sampel tanpa sigmoid.
- Conditioning: one-hot; loss: `BCEWithLogitsLoss`; seed awal: `42`.

Rincian ada di [`docs/architecture.md`](docs/architecture.md) dan urutan kerja/pembagian anggota di [`docs/implementation-plan.md`](docs/implementation-plan.md).

## Tim

1. Ivander Dzaky Khairullah — Prompt Engineer & Model Architect: model dan unit test.
2. Muhammad Ragil — Data Pipeline & Training Engineer: dataset, training, eksperimen.
3. Silmi Sila Nia Uma — Documentation & Evaluation Engineer: evaluasi, visualisasi, dokumentasi.

Aturan kolaborasi dan gerbang implementasi dicatat dalam rencana implementasi.

## Log AI dan evidence

Semua anggota memakai format yang sama dari berbagai platform AI. Salin [`docs/ai-logs/session-template.md`](docs/ai-logs/session-template.md), lalu simpan bukti asli di `evidence/ivander-dzaky-khairullah/`, `evidence/muhammad-ragil/`, atau `evidence/silmi-sila-nia-uma/`. Jangan membuat log atau hasil pengujian fiktif; panduan lengkap: [`docs/ai-logs/README.md`](docs/ai-logs/README.md).

## Data dan artefak

Data lokal berada di `data/`; checkpoint dan hasil eksperimen di `outputs/`. Folder dan file sensitif tersebut dikecualikan dari Git melalui `.gitignore`.
