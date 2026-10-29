# Evaluasi Model

Evaluasi kuantitatif menjawab pertanyaan "apakah gambar generator bisa dikenali sesuai kelasnya" tanpa memakai model pretrained.

## Metode

1. Latih `Classifier` MLP dari data Fashion-MNIST asli (train split) selama 5 epoch, seed 42. Ini classifier pembanding, bukan bagian GAN.
2. Ukur akurasi pada test split asli. Angka ini adalah batas atas kasar: classifier hanya berguna bila cukup akurat pada data asli.
3. Untuk setiap kelas `0..9`, buat 100 gambar dari Generator dengan noise ber-seed tetap, lalu hitung proporsi gambar yang diklasifikasikan sesuai label permintaan.

Akurasi generator yang jauh di bawah akurasi data asli berarti Gambar generator belum menyerupai distribusi kelas tersebut. Angka per kelas memperlihatkan kelas mana yang paling sulit dipelajari.

## Perintah

```bash
python -m fashion_cgan.evaluate outputs/cgan_epoch_50.pt --output-dir outputs/evaluation
```

Opsi: `--epochs` (epoch classifier, default 5), `--samples-per-class` (default 100), `--device`.

## Keluaran

- `evaluation.json`: akurasi data asli, rata-rata akurasi kelas, dan rincian per kelas.
- `evaluation.csv`: tabel per kelas (`class`, `label`, `accuracy`, `samples`).

## Batasan

- Classifier kecil (±200 ribu parameter) dan dilatih singkat; akurasi asli bisa belum optimal.
- Noise generator memakai seed tetap per kelas sehingga hasil dapat direproduksi, tetapi tidak mengukur keragaman mode.
- Metrik ini tidak mengukur kualitas visual; lihat grid sampel dan kurva loss untuk konteks tambahan.
