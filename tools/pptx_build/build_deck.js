/**
 * Build the FashionCGAN final-presentation deck.
 * Run from this directory: node build_deck.js
 */
const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(__dirname, "..", "..");
const FIG = path.join(ROOT, "outputs", "figures");
const OUT = path.join(ROOT, "laporan", "Presentasi-FashionCGAN-Conditional-GAN-MLP.pptx");

const C = {
  navy: "1E2761",
  ice: "CADCFC",
  white: "FFFFFF",
  ink: "1B2236",
  muted: "5D6785",
  accent: "F96167",
  tint: "EEF2FB",
};

const HEAD = "Cambria";
const BODY = "Calibri";
const W = 13.333;
const H = 7.5;

const img = (name) => "image/png;base64," + fs.readFileSync(path.join(FIG, name)).toString("base64");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Ivander Dzaky Khairullah, Muhammad Ragil, Silmi Sila Nia Uma";
pres.title = "FashionCGAN - Conditional GAN MLP untuk Generasi Citra Pakaian";

function titleBar(slide, kicker, title, dark = false) {
  slide.addText(kicker.toUpperCase(), {
    x: 0.6, y: 0.45, w: 8, h: 0.28, margin: 0,
    fontFace: BODY, fontSize: 11, bold: true, charSpacing: 2,
    color: dark ? C.ice : C.accent,
  });
  slide.addText(title, {
    x: 0.6, y: 0.78, w: W - 1.2, h: 0.8, margin: 0,
    fontFace: HEAD, fontSize: 32, bold: true, color: dark ? C.white : C.navy,
  });
}

function footer(slide, page, dark = false) {
  slide.addText("FashionCGAN · Tugas Generative AI", {
    x: 0.6, y: H - 0.55, w: 6, h: 0.25, margin: 0,
    fontFace: BODY, fontSize: 10, color: dark ? C.ice : C.muted,
  });
  slide.addText(String(page), {
    x: W - 1.1, y: H - 0.55, w: 0.5, h: 0.25, margin: 0,
    fontFace: BODY, fontSize: 10, color: dark ? C.ice : C.muted, align: "right",
  });
}

function card(slide, x, y, w, h, fill = C.tint) {
  slide.addShape(pres.ShapeType.roundRect, {
    x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill },
  });
}

function statCard(slide, x, y, w, value, label, color = C.navy) {
  card(slide, x, y, w, 1.55);
  slide.addText(value, {
    x: x + 0.25, y: y + 0.18, w: w - 0.5, h: 0.75, margin: 0,
    fontFace: HEAD, fontSize: 40, bold: true, color,
  });
  slide.addText(label, {
    x: x + 0.25, y: y + 0.95, w: w - 0.5, h: 0.5, margin: 0,
    fontFace: BODY, fontSize: 12, color: C.muted,
  });
}

function bullets(items, size = 16) {
  return items.map((text, i) => ({
    text,
    options: {
      bullet: true, breakLine: i < items.length - 1,
      fontFace: BODY, fontSize: size, color: C.ink, paraSpaceAfter: 10,
    },
  }));
}

// 1 — Title (dark)
{
  const s = pres.addSlide();
  s.background = { color: C.navy };
  s.addText("TUGAS MATA KULIAH GENERATIVE AI", {
    x: 0.9, y: 1.0, w: 11, h: 0.3, margin: 0,
    fontFace: BODY, fontSize: 12, bold: true, charSpacing: 2.5, color: C.ice,
  });
  s.addText("Conditional GAN Berbasis MLP\nuntuk Generasi Citra Pakaian\nFashion-MNIST", {
    x: 0.9, y: 1.5, w: 11.5, h: 2.9, margin: 0,
    fontFace: HEAD, fontSize: 40, bold: true, color: C.white, lineSpacing: 48,
  });
  s.addText(
    [
      { text: "Ivander Dzaky Khairullah (103012300174)", options: { breakLine: true } },
      { text: "Muhammad Ragil (103012300015)", options: { breakLine: true } },
      { text: "Silmi Sila Nia Uma (103012430070)", options: {} },
    ],
    { x: 0.9, y: 4.85, w: 7.2, h: 1.1, margin: 0, fontFace: BODY, fontSize: 15, color: C.white },
  );
  s.addText("Dosen Pengampu: Dr. Aditya Firman Ihsan, S.Si., M.Si.", {
    x: 0.9, y: 6.1, w: 8.5, h: 0.3, margin: 0, fontFace: BODY, fontSize: 13, color: C.ice,
  });
  s.addText("2026", {
    x: W - 1.9, y: 6.1, w: 1.0, h: 0.3, margin: 0,
    fontFace: HEAD, fontSize: 16, bold: true, color: C.white, align: "right",
  });
}

// 2 — Agenda
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Agenda", "Apa yang akan dibahas");
  const items = [
    ["01", "Latar belakang", "Mengapa cGAN dan Fashion-MNIST"],
    ["02", "Arsitektur", "Generator & Discriminator MLP"],
    ["03", "Pelatihan", "Konfigurasi, loss, dan alur"],
    ["04", "Hasil visual", "Progres epoch dan sampel per kelas"],
    ["05", "Evaluasi", "Akurasi classifier per kelas"],
    ["06", "Kesimpulan", "Temuan, batasan, dan saran"],
  ];
  items.forEach(([num, head, sub], i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.6 + col * 6.1;
    const y = 1.95 + row * 1.55;
    card(s, x, y, 5.8, 1.3);
    s.addText(num, {
      x: x + 0.3, y: y + 0.28, w: 0.9, h: 0.6, margin: 0,
      fontFace: HEAD, fontSize: 30, bold: true, color: C.accent,
    });
    s.addText(head, {
      x: x + 1.25, y: y + 0.24, w: 4.3, h: 0.4, margin: 0,
      fontFace: BODY, fontSize: 17, bold: true, color: C.navy,
    });
    s.addText(sub, {
      x: x + 1.25, y: y + 0.68, w: 4.3, h: 0.4, margin: 0,
      fontFace: BODY, fontSize: 13, color: C.muted,
    });
  });
  footer(s, 2);
}

// 3 — Latar belakang
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Latar belakang", "Masalah dan tujuan");
  s.addText(bullets([
    "GAN melatih dua jaringan berlawanan: Generator membuat gambar, Discriminator menilai keasliannya.",
    "GAN dasar tidak bisa diminta membuat kelas tertentu, sehingga perlu conditioning label (cGAN).",
    "Implementasi konvolusional bergantung pada model pretrained; mekanisme dasarnya jadi tersembunyi.",
    "Penilaian kualitas butuh metrik terpisah, karena loss adversarial hanya mengukur keseimbangan D dan G.",
  ]), { x: 0.6, y: 1.95, w: 6.4, h: 3.6, margin: 0 });
  card(s, 7.3, 1.9, 5.4, 4.3, C.navy);
  s.addText("Tujuan", {
    x: 7.65, y: 2.15, w: 4.7, h: 0.45, margin: 0,
    fontFace: HEAD, fontSize: 22, bold: true, color: C.white,
  });
  s.addText(bullets([
    "cGAN MLP dari komponen dasar PyTorch",
    "Pipeline reproducible (seed & konfigurasi tercatat)",
    "Evaluasi tanpa model pretrained",
    "Mengidentifikasi kelas yang sulit dipelajari",
  ], 14).map((t) => ({ ...t, options: { ...t.options, color: C.ice } })), {
    x: 7.65, y: 2.85, w: 4.7, h: 3.1, margin: 0,
  });
  footer(s, 3);
}

// 4 — Dataset
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Dataset", "Fashion-MNIST: 10 kelas, 60.000 citra latih");
  s.addImage({ data: img("dataset_samples.png"), x: 0.6, y: 1.95, w: 6.6, h: 2.8 });
  s.addText("Gambar 1. Satu contoh citra per kelas", {
    x: 0.6, y: 4.8, w: 6.6, h: 0.25, margin: 0,
    fontFace: BODY, fontSize: 10, italic: true, color: C.muted,
  });
  statCard(s, 7.5, 1.95, 2.6, "28×28", "piksel grayscale");
  statCard(s, 10.3, 1.95, 2.4, "10", "kelas pakaian");
  statCard(s, 7.5, 3.75, 2.6, "60.000", "citra latih (6.000/kelas)");
  statCard(s, 10.3, 3.75, 2.4, "10.000", "citra uji");
  s.addText("Distribusi kelas seimbang, sehingga perbedaan kualitas antarkelas dipengaruhi bentuk, bukan jumlah data.", {
    x: 7.5, y: 5.55, w: 5.2, h: 0.7, margin: 0,
    fontFace: BODY, fontSize: 13, italic: true, color: C.ink,
  });
  footer(s, 4);
}

// 5 — Arsitektur (dark)
{
  const s = pres.addSlide();
  s.background = { color: C.navy };
  titleBar(s, "Arsitektur", "Conditioning label pada kedua jaringan", true);

  const box = (x, y, w, h, text, fill = "2A3475", size = 12) => {
    s.addShape(pres.ShapeType.roundRect, {
      x, y, w, h, rectRadius: 0.06, fill: { color: fill }, line: { color: fill },
    });
    s.addText(text, {
      x, y: y + h / 2 - 0.32, w, h: 0.64, margin: 0, align: "center", valign: "middle",
      fontFace: BODY, fontSize: size, color: C.white,
    });
  };

  s.addText("Generator", { x: 0.6, y: 1.75, w: 5, h: 0.3, margin: 0, fontFace: HEAD, fontSize: 16, bold: true, color: C.ice });
  const gx = 0.6;
  box(gx, 2.15, 2.0, 0.8, "Noise z\n(100)", "3C4A8C");
  box(gx + 2.15, 2.15, 2.1, 0.8, "Label y\none-hot (10)", "3C4A8C");
  box(gx, 3.25, 4.25, 0.7, "Concat 110 → Linear 256 (ReLU)", "2A3475");
  box(gx, 4.05, 4.25, 0.7, "Linear 512 (ReLU)", "2A3475");
  box(gx, 4.85, 4.25, 0.7, "Linear 784 + tanh", "F96167", 12);
  box(gx, 5.65, 4.25, 0.7, "Reshape 1×28×28", "3C4A8C");

  s.addText("Discriminator", { x: 7.1, y: 1.75, w: 5, h: 0.3, margin: 0, fontFace: HEAD, fontSize: 16, bold: true, color: C.ice });
  const dx = 7.1;
  box(dx, 2.15, 2.0, 0.8, "Gambar\n(784)", "3C4A8C");
  box(dx + 2.15, 2.15, 2.1, 0.8, "Label y\none-hot (10)", "3C4A8C");
  box(dx, 3.25, 4.25, 0.7, "Concat 794 → Linear 512 (LeakyReLU)", "2A3475");
  box(dx, 4.05, 4.25, 0.7, "Linear 256 (LeakyReLU)", "2A3475");
  box(dx, 4.85, 4.25, 0.7, "Linear 1 (logit, tanpa sigmoid)", "F96167", 12);
  box(dx, 5.65, 4.25, 0.7, "BCEWithLogitsLoss", "3C4A8C");

  footer(s, 5, true);
}

// 6 — Prosedur pelatihan
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Pelatihan", "Satu iterasi, dua kali pembaruan");
  const steps = [
    ["1", "Latih Discriminator", "Asli → target 1, palsu → target 0, lalu backward dan step."],
    ["2", "Bekukan Discriminator", "Semua parameter requires_grad=False saat update Generator."],
    ["3", "Latih Generator", "Hasil palsu dinilai D, target 1 agar menipu Discriminator."],
    ["4", "Catat & simpan", "Checkpoint per epoch dan metrics.csv untuk analisis."],
  ];
  steps.forEach(([num, head, sub], i) => {
    const y = 1.85 + i * 1.22;
    s.addShape(pres.ShapeType.ellipse, {
      x: 0.6, y, w: 0.7, h: 0.7, fill: { color: i % 2 ? C.accent : C.navy }, line: { color: C.navy, width: 0 },
    });
    s.addText(num, {
      x: 0.6, y: y + 0.12, w: 0.7, h: 0.45, margin: 0, align: "center",
      fontFace: HEAD, fontSize: 18, bold: true, color: C.white,
    });
    s.addText(head, {
      x: 1.55, y: y + 0.02, w: 4.3, h: 0.35, margin: 0,
      fontFace: BODY, fontSize: 17, bold: true, color: C.navy,
    });
    s.addText(sub, {
      x: 1.55, y: y + 0.38, w: 4.8, h: 0.45, margin: 0,
      fontFace: BODY, fontSize: 13, color: C.muted,
    });
  });
  card(s, 6.8, 1.85, 5.9, 3.9);
  s.addText("Konfigurasi", {
    x: 7.1, y: 2.05, w: 5.3, h: 0.35, margin: 0,
    fontFace: HEAD, fontSize: 18, bold: true, color: C.navy,
  });
  const cfg = [
    ["Optimizer", "Adam, lr 2e-4, betas (0.5; 0.999)"],
    ["Loss", "BCEWithLogitsLoss"],
    ["Batch / Epoch", "128 / 50"],
    ["Perangkat", "CPU (tanpa GPU)"],
    ["Seed", "42 (Python, NumPy, PyTorch, shuffle)"],
    ["Durasi", "1.061,2 detik"],
  ];
  cfg.forEach(([k, v], i) => {
    const y = 2.55 + i * 0.5;
    s.addText(k, { x: 7.1, y, w: 1.7, h: 0.35, margin: 0, fontFace: BODY, fontSize: 13, bold: true, color: C.ink });
    s.addText(v, { x: 8.85, y, w: 3.6, h: 0.35, margin: 0, fontFace: BODY, fontSize: 13, color: C.muted });
  });
  footer(s, 6);
}

// 7 — Loss
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Hasil pelatihan", "Loss D dan G seimbang di paruh akhir");

  const epochs = Array.from({ length: 50 }, (_, i) => i + 1);
  const D = [0.358, 0.396, 0.428, 0.399, 0.449, 0.553, 0.645, 0.669, 0.675, 0.782, 0.853, 0.861, 0.91, 0.958, 0.948, 1.0, 1.033, 1.045, 1.052, 1.057, 1.066, 1.095, 1.136, 1.152, 1.131, 1.158, 1.17, 1.176, 1.188, 1.2, 1.191, 1.198, 1.201, 1.209, 1.208, 1.227, 1.228, 1.23, 1.23, 1.241, 1.251, 1.245, 1.244, 1.25, 1.249, 1.251, 1.252, 1.256, 1.256, 1.261];
  const G = [3.212, 5.212, 3.682, 3.715, 3.714, 3.351, 2.81, 2.791, 2.595, 2.311, 2.025, 1.988, 1.856, 1.754, 1.791, 1.646, 1.535, 1.481, 1.509, 1.508, 1.451, 1.374, 1.294, 1.278, 1.264, 1.261, 1.208, 1.164, 1.146, 1.138, 1.134, 1.131, 1.103, 1.099, 1.082, 1.065, 1.05, 1.052, 1.013, 1.004, 0.989, 0.998, 0.992, 0.971, 0.98, 0.975, 0.97, 0.96, 0.948, 0.956];

  s.addChart(
    pres.ChartType.line,
    [
      { name: "Discriminator", labels: epochs.map(String), values: D },
      { name: "Generator", labels: epochs.map(String), values: G },
    ],
    {
      x: 0.5, y: 1.8, w: 8.2, h: 4.6,
      showTitle: false,
      chartColors: [C.navy, C.accent],
      lineSize: 2,
      showLegend: true,
      legendPos: "b",
      legendColor: C.ink,
      catAxisLabelColor: C.muted,
      catAxisLabelFontSize: 10,
      valAxisLabelColor: C.muted,
      valAxisLabelFontSize: 10,
      catAxisTitle: "epoch",
      catAxisTitleColor: C.muted,
      catAxisTitleFontSize: 11,
      valAxisTitle: "BCEWithLogitsLoss",
      valAxisTitleColor: C.muted,
      valAxisTitleFontSize: 11,
      valGridLine: { color: "E3E7F1", size: 1 },
      catGridLine: { style: "none" },
    },
  );
  statCard(s, 9.1, 1.9, 3.6, "1,2613", "loss D akhir (epoch 50)", C.navy);
  statCard(s, 9.1, 3.65, 3.6, "0,9564", "loss G akhir (epoch 50)", C.accent);
  s.addText("Loss adversarial mengukur keseimbangan kedua jaringan, bukan kualitas gambar.", {
    x: 9.1, y: 5.45, w: 3.6, h: 0.8, margin: 0,
    fontFace: BODY, fontSize: 12, italic: true, color: C.muted,
  });
  footer(s, 7);
}

// 8 — Progres visual
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Progres visual", "Bentuk muncul dari epoch ke epoch");
  s.addImage({ data: img("progression_by_epoch.png"), x: 1.15, y: 1.75, w: 6.4, h: 4.8 });
  s.addText("Gambar 2. Keluaran Generator pada epoch 1, 25, dan 50 dengan noise tetap", {
    x: 0.6, y: 6.62, w: 7.6, h: 0.25, margin: 0,
    fontFace: BODY, fontSize: 10, italic: true, color: C.muted,
  });
  card(s, 8.1, 1.9, 4.6, 4.4);
  s.addText("Yang berubah", {
    x: 8.4, y: 2.1, w: 4.0, h: 0.35, margin: 0,
    fontFace: HEAD, fontSize: 18, bold: true, color: C.navy,
  });
  s.addText(bullets([
    "Epoch 1: gumpalan abu-abu tanpa siluet.",
    "Epoch 25: kaus, tas, dan sepatu mulai jelas.",
    "Epoch 50: kontras dan siluet lebih tegas.",
    "Derau di latar masih tersisa.",
  ], 14), { x: 8.4, y: 2.6, w: 4.0, h: 3.4, margin: 0 });
  footer(s, 8);
}

// 9 — Sampel per kelas
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Kualitas hasil", "Empat sampel per kelas (epoch 50)");
  s.addImage({ data: img("samples_per_class.png"), x: 0.75, y: 1.72, w: 3.9, h: 5.0 });
  card(s, 5.0, 1.9, 3.75, 2.0);
  s.addText("Kelas berhasil", {
    x: 5.25, y: 2.05, w: 3.3, h: 0.3, margin: 0,
    fontFace: BODY, fontSize: 15, bold: true, color: C.navy,
  });
  s.addText("Trouser · Bag · Sneaker · Ankle boot\nsiluet khas, mudah dikenali", {
    x: 5.25, y: 2.4, w: 3.3, h: 1.3, margin: 0,
    fontFace: BODY, fontSize: 13, color: C.muted,
  });
  card(s, 8.95, 1.9, 3.75, 2.0);
  s.addText("Kelas sulit", {
    x: 9.2, y: 2.05, w: 3.3, h: 0.3, margin: 0,
    fontFace: BODY, fontSize: 15, bold: true, color: C.accent,
  });
  s.addText("Shirt · Coat · Pullover · Dress\nsiluet beririsan, sering tertukar", {
    x: 9.2, y: 2.4, w: 3.3, h: 1.3, margin: 0,
    fontFace: BODY, fontSize: 13, color: C.muted,
  });
  s.addText(
    "Tanpa lapisan konvolusi, Generator hanya menangkap pola global, bukan tekstur dan detail tepi.",
    { x: 5.0, y: 4.25, w: 7.7, h: 1.0, margin: 0, fontFace: BODY, fontSize: 14, italic: true, color: C.ink },
  );
  footer(s, 9);
}

// 10 — Keragaman
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Keragaman", "Tidak terjadi mode collapse total");
  s.addImage({ data: img("diversity_per_class.png"), x: 0.6, y: 1.95, w: 8.2, h: 3.1 });
  s.addText("Gambar 3. Dua belas sampel per kelas (T-shirt, Dress, Shirt, Sneaker)", {
    x: 0.6, y: 5.15, w: 8.2, h: 0.25, margin: 0,
    fontFace: BODY, fontSize: 10, italic: true, color: C.muted,
  });
  card(s, 9.1, 1.9, 3.6, 3.6);
  s.addText("Pengamatan", {
    x: 9.35, y: 2.1, w: 3.1, h: 0.3, margin: 0,
    fontFace: HEAD, fontSize: 17, bold: true, color: C.navy,
  });
  s.addText(bullets([
    "Variasi kemiringan lengan terlihat.",
    "Bentuk sol Sneaker beragam.",
    "Ragam lebih sempit dari data asli.",
  ], 13), { x: 9.35, y: 2.55, w: 3.1, h: 2.7, margin: 0 });
  footer(s, 10);
}

// 11 — Evaluasi kuantitatif
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Evaluasi", "Classifier menilai kesesuaian kelas");
  statCard(s, 0.6, 1.85, 3.0, "0,8755", "akurasi data asli", C.navy);
  statCard(s, 3.8, 1.85, 3.0, "0,8670", "rata-rata generator", C.accent);
  statCard(s, 7.0, 1.85, 3.0, "1,00", "terbaik: Trouser", C.navy);
  statCard(s, 10.2, 1.85, 2.5, "0,62", "terlemah: Shirt", C.accent);

  s.addImage({ data: img("classifier_accuracy.png"), x: 0.6, y: 3.65, w: 7.4, h: 3.3 });
  s.addText("Metode: MLP classifier dilatih dari data asli (5 epoch), lalu 100 gambar per kelas diuji.", {
    x: 8.3, y: 3.75, w: 4.4, h: 1.0, margin: 0,
    fontFace: BODY, fontSize: 13, color: C.ink,
  });
  s.addText("Selisih 0,0085 terhadap data asli menunjukkan mayoritas gambar generator sudah dikenali sesuai kelasnya, meski classifier berkapasitas kecil.", {
    x: 8.3, y: 4.9, w: 4.4, h: 1.6, margin: 0,
    fontFace: BODY, fontSize: 12, italic: true, color: C.muted,
  });
  footer(s, 11);
}

// 12 — Kesimpulan (dark)
{
  const s = pres.addSlide();
  s.background = { color: C.navy };
  titleBar(s, "Kesimpulan", "Temuan utama", true);
  const pts = [
    ["Conditioning bekerja", "Label one-hot mengubah bentuk keluaran; kelas bersiluet khas unggul."],
    ["Reproducible", "Seed 42, konfigurasi YAML, 50 epoch CPU dalam 1.061,2 detik."],
    ["Kualitas terukur", "Akurasi generator 0,8670 vs data asli 0,8755."],
    ["Batasan MLP", "Detail tepi dan kelas mirip (Shirt, Coat) masih lemah."],
  ];
  pts.forEach(([head, sub], i) => {
    const y = 1.85 + i * 1.15;
    s.addShape(pres.ShapeType.roundRect, {
      x: 0.6, y, w: 12.1, h: 0.98, rectRadius: 0.06, fill: { color: "2A3475" }, line: { color: "2A3475" },
    });
    s.addText(head, {
      x: 0.95, y: y + 0.12, w: 4.0, h: 0.35, margin: 0,
      fontFace: BODY, fontSize: 16, bold: true, color: C.white,
    });
    s.addText(sub, {
      x: 0.95, y: y + 0.48, w: 11.4, h: 0.4, margin: 0,
      fontFace: BODY, fontSize: 13, color: C.ice,
    });
  });
  footer(s, 12, true);
}

// 13 — Pengembangan
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  titleBar(s, "Pengembangan", "Langkah berikutnya");
  const items = [
    ["CNN / DCGAN", "Lapisan konvolusi untuk detail tepi dan tekstur."],
    ["Metrik keragaman", "Ukur mode collapse secara kuantitatif tanpa pretrained."],
    ["Classifier lebih kuat", "Kapasitas lebih besar agar cacat lokal tertangkap."],
    ["Eksperimen lanjutan", "Kontrak data tetap, arsitektur diuji terpisah."],
  ];
  items.forEach(([head, sub], i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.6 + col * 6.15;
    const y = 1.95 + row * 2.15;
    card(s, x, y, 5.85, 1.85);
    s.addText(head, {
      x: x + 0.3, y: y + 0.28, w: 5.2, h: 0.4, margin: 0,
      fontFace: HEAD, fontSize: 19, bold: true, color: C.navy,
    });
    s.addText(sub, {
      x: x + 0.3, y: y + 0.85, w: 5.2, h: 0.75, margin: 0,
      fontFace: BODY, fontSize: 13, color: C.muted,
    });
  });
  footer(s, 13);
}

// 14 — Penutup
{
  const s = pres.addSlide();
  s.background = { color: C.navy };
  s.addText("Terima kasih", {
    x: 0.9, y: 2.4, w: 11.5, h: 1.1, margin: 0,
    fontFace: HEAD, fontSize: 48, bold: true, color: C.white,
  });
  s.addText("Pertanyaan dan diskusi", {
    x: 0.9, y: 3.55, w: 11.5, h: 0.5, margin: 0,
    fontFace: BODY, fontSize: 18, color: C.ice,
  });
  s.addText(
    "Ivander Dzaky Khairullah · Muhammad Ragil · Silmi Sila Nia Uma",
    { x: 0.9, y: 5.9, w: 11.5, h: 0.3, margin: 0, fontFace: BODY, fontSize: 13, color: C.ice },
  );
  s.addText("github.com/IvanderDzaky/FashionCGAN", {
    x: 0.9, y: 6.25, w: 11.5, h: 0.3, margin: 0, fontFace: BODY, fontSize: 12, color: "8FA2D6",
  });
}

// Speaker notes
const notes = {
  1: "Perkenalkan anggota dan judul. Sebut bahwa seluruh model dibangun dari komponen dasar PyTorch tanpa model pretrained.",
  3: "Tekankan celah: implementasi populer menyembunyikan mekanisme dasar, dan loss adversarial tidak mengukur kualitas.",
  4: "Distribusi kelas seimbang sehingga perbedaan hasil antarkelas bukan efek jumlah data.",
  5: "Jelaskan alur tensor: noise 100 + one-hot 10 = 110 masuk Generator; gambar 784 + one-hot 10 = 794 masuk Discriminator.",
  6: "Sebut pembekuan parameter Discriminator saat update Generator untuk mencegah perubahan bersamaan.",
  7: "Garis D naik lalu stabil, G turun. Ingatkan bahwa loss bukan metrik kualitas.",
  8: "Bandingkan tiga epoch dengan noise yang sama agar perbandingan adil.",
  9: "Sebut kelas yang gagal jelas: Shirt sering tertukar dengan Coat/Pullover.",
  10: "Tunjukkan variasi lengan dan sol; sebut ragam masih lebih sempit dari data asli.",
  11: "Jelaskan classifier dilatih terpisah dari data asli, lalu dipakai sebagai penilai.",
  12: "Rangkum empat temuan, hubungkan kembali dengan rumusan masalah.",
  13: "Sebut CNN sebagai eksperimen terpisah tanpa mengubah kontrak data.",
};

pres.slides.forEach((slide, i) => {
  const text = notes[i + 1];
  if (text) slide.addNotes(text);
});

pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
