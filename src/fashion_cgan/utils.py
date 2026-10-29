"""Shared helpers for evaluation and visualization."""

from collections.abc import Iterable, Sequence
from pathlib import Path

import torch

FASHION_MNIST_CLASSES = (
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
)


def denormalize(images: torch.Tensor) -> torch.Tensor:
    """Map images from [-1, 1] to [0, 1] for saving or display."""
    if not isinstance(images, torch.Tensor):
        raise TypeError("images must be a tensor")
    return (images.clamp(-1, 1) + 1) / 2


def load_metrics(path: str | Path) -> list[dict[str, float | int]]:
    """Read a training metrics CSV into a list of typed rows."""
    import csv

    with Path(path).open(encoding="utf-8", newline="") as metrics_file:
        rows = list(csv.DictReader(metrics_file))
    return [
        {
            "epoch": int(row["epoch"]),
            "discriminator_loss": float(row["discriminator_loss"]),
            "generator_loss": float(row["generator_loss"]),
        }
        for row in rows
    ]


def save_image_grid(
    images: torch.Tensor,
    output_path: str | Path,
    labels: Sequence[int] | None = None,
    nrow: int = 10,
) -> Path:
    """Save images in [-1, 1] as a PNG grid and return the output path."""
    from torchvision.utils import save_image

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_image(denormalize(images), output_path, nrow=nrow)
    if labels is not None:
        label_path = output_path.with_suffix(".labels.txt")
        label_path.write_text("\n".join(str(label) for label in labels) + "\n", encoding="utf-8")
    return output_path


def class_names(labels: Iterable[int]) -> list[str]:
    """Map class indices to Fashion-MNIST class names."""
    names = []
    for label in labels:
        if not 0 <= label < len(FASHION_MNIST_CLASSES):
            raise ValueError(f"labels must be in the range 0..{len(FASHION_MNIST_CLASSES) - 1}")
        names.append(FASHION_MNIST_CLASSES[label])
    return names
