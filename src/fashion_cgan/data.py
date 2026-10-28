"""Fashion-MNIST dataset and DataLoader helpers."""

from pathlib import Path

import torch
from torch.utils.data import DataLoader


def get_dataloaders(
    root: str | Path = "data",
    batch_size: int = 128,
    download: bool = True,
    num_workers: int = 0,
    seed: int = 42,
) -> tuple[DataLoader, DataLoader]:
    """Return train and test loaders with images normalized to [-1, 1]."""
    if batch_size < 1:
        raise ValueError("batch_size must be positive")
    if num_workers < 0:
        raise ValueError("num_workers must be non-negative")
    from torchvision import datasets, transforms

    transform = transforms.Compose((transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))))
    train_dataset = datasets.FashionMNIST(root=root, train=True, download=download, transform=transform)
    test_dataset = datasets.FashionMNIST(root=root, train=False, download=download, transform=transform)
    # Fixed generator keeps the shuffle order reproducible across runs.
    return (
        DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            generator=torch.Generator().manual_seed(seed),
        ),
        DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers),
    )
