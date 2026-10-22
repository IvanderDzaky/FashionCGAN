# Rancangan Arsitektur

## Tujuan

Membangun conditional GAN MLP dari komponen dasar PyTorch untuk menghasilkan Fashion-MNIST grayscale berukuran 28×28 pada 10 kelas. Model pretrained dan implementasi GAN siap pakai tidak digunakan.

## Komponen dan keputusan

- Conditioning label menggunakan one-hot vektor berdimensi 10, digabung dengan noise pada Generator dan representasi gambar pada Discriminator.
- Noise Generator berbentuk `[B, 100]`; label integer berbentuk `[B]` dengan rentang `0..9`.
- Generator menggunakan lapisan `Linear` dan ReLU, lalu output 784 unit dengan `Tanh`, dibentuk menjadi `[B, 1, 28, 28]`.
- Discriminator menerima gambar `[B, 1, 28, 28]` dan label `[B]`; MLP mengeluarkan satu logit per sampel `[B, 1]`.
- Gunakan `BCEWithLogitsLoss`; Discriminator mengembalikan logits tanpa sigmoid.
- Dataset mengubah intensitas gambar ke `[-1, 1]`, selaras dengan `Tanh` Generator.
- Seed awal `42`. Reproducibility juga memerlukan pengaturan generator NumPy/PyTorch, DataLoader, dan backend deterministik sesuai dukungan perangkat. Determinisme penuh dapat mengurangi kecepatan dan tidak selalu identik lintas perangkat/versi.

## Kontrak modul

| Modul | Input | Output |
|---|---|---|
| Dataset/DataLoader | Fashion-MNIST | gambar float `[B,1,28,28]` dalam `[-1,1]`; label integer `[B]`, `0..9` |
| Generator | noise `[B,100]`; label `[B]` | gambar `[B,1,28,28]` dalam `[-1,1]` |
| Discriminator | gambar `[B,1,28,28]`; label `[B]` | logits `[B,1]` |
| Training loop | batch gambar/label dan model | optimasi D lalu G; loss/metrik; checkpoint bila ditambahkan |

`B` berarti ukuran batch yang sama pada satu forward pass. Device dan tipe tensor harus konsisten.

## Rencana uji model

1. Bentuk output Generator dan Discriminator benar untuk batch kecil serta batch satu.
2. Output Generator finite dan berada pada rentang `[-1,1]`.
3. Output Discriminator finite dan berbentuk satu logit per gambar.
4. **Conditioning label:** dengan bobot tetap dan noise/gambar yang sama, uji bahwa perubahan label masuk ke jalur conditioning; gunakan pengujian sensitivitas eksplisit setelah arsitektur ditetapkan. Tes tidak boleh mengasumsikan output acak pasti berbeda tanpa mengontrol bobot.
5. **Gradient flow:** loss sintetis dirambatkan melalui masing-masing model; pastikan parameter yang dapat dilatih mendapat gradient finite dan tidak seluruhnya nol.
6. Tes kontrak data: bentuk, dtype, rentang normalisasi, dan label valid.

## Trade-off

MLP sederhana dan mudah diinspeksi, cocok untuk baseline akademik. Ia tidak memanfaatkan struktur spasial sebaik CNN; bila hasil baseline tidak memadai, perubahan arsitektur dilakukan sebagai eksperimen terpisah dan didokumentasikan.
