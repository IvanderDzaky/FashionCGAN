"""Fashion-MNIST dataset and DataLoader helpers."""

from pathlib import Path

from torch.utils.data import DataLoader


def get_dataloaders(
    root: str | Path = "data", batch_size: int = 128, download: bool = True
) -> tuple[DataLoader, DataLoader]:
    """Return train and test loaders with images normalized to [-1, 1]."""
    from torchvision import datasets, transforms

    transform = transforms.Compose((transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))))
    train_dataset = datasets.FashionMNIST(root=root, train=True, download=download, transform=transform)
    test_dataset = datasets.FashionMNIST(root=root, train=False, download=download, transform=transform)
    return (
        DataLoader(train_dataset, batch_size=batch_size, shuffle=True),
        DataLoader(test_dataset, batch_size=batch_size, shuffle=False),
    )
