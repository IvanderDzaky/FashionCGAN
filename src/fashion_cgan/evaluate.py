"""Evaluate a trained conditional GAN with a Fashion-MNIST classifier."""

import argparse
import json
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F

from fashion_cgan.models import Generator
from fashion_cgan.utils import class_names


class Classifier(nn.Module):
    """Small MLP classifier trained from scratch on real Fashion-MNIST images."""

    def __init__(self, num_classes: int = 10) -> None:
        super().__init__()
        self.num_classes = num_classes
        self.network = nn.Sequential(
            nn.Linear(28 * 28, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, num_classes),
        )

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        if images.ndim != 4 or tuple(images.shape[1:]) != (1, 28, 28):
            raise ValueError("images must have shape [B, 1, 28, 28]")
        return self.network(images.flatten(start_dim=1))


def train_classifier(
    train_loader,
    epochs: int = 5,
    device: str | torch.device = "cpu",
    learning_rate: float = 1e-3,
    seed: int = 42,
) -> Classifier:
    """Train the evaluation classifier on the real training split."""
    if epochs < 1:
        raise ValueError("epochs must be positive")
    torch.manual_seed(seed)
    device = torch.device(device)
    classifier = Classifier().to(device)
    optimizer = torch.optim.Adam(classifier.parameters(), lr=learning_rate)
    for _ in range(epochs):
        classifier.train()
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device, dtype=torch.long)
            optimizer.zero_grad(set_to_none=True)
            loss = F.cross_entropy(classifier(images), labels)
            loss.backward()
            optimizer.step()
    return classifier


@torch.inference_mode()
def classifier_accuracy(classifier: Classifier, loader, device: str | torch.device = "cpu") -> float:
    """Fraction of correctly classified images in a loader."""
    device = torch.device(device)
    classifier.eval()
    correct = total = 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device, dtype=torch.long)
        predictions = classifier(images).argmax(dim=1)
        correct += int((predictions == labels).sum().item())
        total += labels.numel()
    if not total:
        raise ValueError("loader produced no samples")
    return correct / total


@torch.inference_mode()
def generated_class_accuracy(
    classifier: Classifier,
    generator: Generator,
    labels: list[int],
    samples_per_class: int = 100,
    latent_dim: int = 100,
    num_classes: int = 10,
    device: str | torch.device = "cpu",
    seed: int = 42,
) -> dict[str, dict[str, float | int | str]]:
    """Generate images per requested class and report the classifier agreement."""
    if samples_per_class < 1:
        raise ValueError("samples_per_class must be positive")
    if not labels:
        raise ValueError("at least one label is required")
    device = torch.device(device)
    generator_device = torch.device(next(generator.parameters()).device)
    classifier.to(device).eval()
    generator.to(generator_device).eval()
    target = torch.cat([torch.full((samples_per_class,), label) for label in labels])
    if torch.any((target < 0) | (target >= num_classes)).item():
        raise ValueError(f"labels must be in the range 0..{num_classes - 1}")

    results: dict[str, dict[str, float | int | str]] = {}
    for index, name in enumerate(class_names(labels)):
        chunk = target[index * samples_per_class : (index + 1) * samples_per_class]
        noise = torch.randn(
            chunk.shape[0], latent_dim, generator=torch.Generator().manual_seed(seed), device=generator_device
        )
        images = generator(noise, chunk.to(generator_device)).to(device)
        predictions = classifier(images).argmax(dim=1)
        results[name] = {
            "label": int(chunk[0]),
            "accuracy": float((predictions == chunk.to(device)).float().mean().item()),
            "samples": int(chunk.shape[0]),
        }
    return results


def evaluate(
    checkpoint_path: str | Path,
    output_dir: str | Path = "outputs/evaluation",
    epochs: int = 5,
    samples_per_class: int = 100,
    device: str | torch.device | None = None,
    download: bool = True,
) -> dict[str, object]:
    """Train the classifier, measure real vs generated accuracy, and save a report."""
    import csv

    from fashion_cgan.data import get_dataloaders

    device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    config = checkpoint["config"]
    seed = config["seed"]
    train_loader, test_loader = get_dataloaders(
        config["data"]["root"], config["training"]["batch_size"], download, seed=seed
    )
    classifier = train_classifier(train_loader, epochs, device, seed=seed)
    real_accuracy = classifier_accuracy(classifier, test_loader, device)

    generator = Generator(config["model"]["latent_dim"], config["data"]["classes"]).to(device)
    generator.load_state_dict(checkpoint["generator"])
    generated = generated_class_accuracy(
        classifier,
        generator,
        list(range(config["data"]["classes"])),
        samples_per_class,
        config["model"]["latent_dim"],
        config["data"]["classes"],
        device,
        seed,
    )

    report = {
        "checkpoint": str(checkpoint_path),
        "epoch": int(checkpoint.get("epoch", 0)),
        "device": str(device),
        "real_accuracy": round(real_accuracy, 4),
        "generated_accuracy_mean": round(
            sum(item["accuracy"] for item in generated.values()) / len(generated), 4
        ),
        "generated": {name: {**item, "accuracy": round(item["accuracy"], 4)} for name, item in generated.items()},
    }

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evaluation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "evaluation.csv").open("w", newline="", encoding="utf-8") as report_file:
        writer = csv.writer(report_file)
        writer.writerow(["class", "label", "accuracy", "samples"])
        for name, item in report["generated"].items():
            writer.writerow([name, item["label"], item["accuracy"], item["samples"]])
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", help="Path to a checkpoint saved by fashion_cgan.train")
    parser.add_argument("--output-dir", default="outputs/evaluation")
    parser.add_argument("--epochs", type=int, default=5, help="Classifier training epochs")
    parser.add_argument("--samples-per-class", type=int, default=100)
    parser.add_argument("--device")
    args = parser.parse_args()
    report = evaluate(
        args.checkpoint, args.output_dir, args.epochs, args.samples_per_class, args.device
    )
    print(
        f"real accuracy: {report['real_accuracy']:.4f}; "
        f"generated accuracy mean: {report['generated_accuracy_mean']:.4f}"
    )


if __name__ == "__main__":
    main()
