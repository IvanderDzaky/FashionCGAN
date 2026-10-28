import sys
import types

import pytest
import torch
from torch.utils.data import TensorDataset

from fashion_cgan.data import get_dataloaders
from fashion_cgan.models import Discriminator, Generator


@pytest.fixture
def fake_torchvision(monkeypatch):
    class ToTensor:
        def __call__(self, image):
            return torch.as_tensor(image, dtype=torch.float32).unsqueeze(0) / 255

    class Normalize:
        def __init__(self, mean, std):
            self.mean, self.std = mean[0], std[0]

        def __call__(self, image):
            return (image - self.mean) / self.std

    class Compose:
        def __init__(self, transforms):
            self.transforms = transforms

        def __call__(self, image):
            for transform in self.transforms:
                image = transform(image)
            return image

    class FashionMNIST:
        def __new__(cls, root, train, download, transform):
            images = torch.arange(4 * 28 * 28).remainder(256).to(torch.uint8).reshape(4, 28, 28)
            labels = torch.arange(4)
            return TensorDataset(torch.stack([transform(image) for image in images]), labels)

    module = types.ModuleType("torchvision")
    module.datasets = types.SimpleNamespace(FashionMNIST=FashionMNIST)
    module.transforms = types.SimpleNamespace(ToTensor=ToTensor, Normalize=Normalize, Compose=Compose)
    monkeypatch.setitem(sys.modules, "torchvision", module)


def test_fashion_mnist_batches_match_model_contract(fake_torchvision):
    train_loader, test_loader = get_dataloaders(batch_size=2)
    images, labels = next(iter(train_loader))

    assert images.shape == (2, 1, 28, 28)
    assert images.dtype == torch.float32
    assert -1 <= images.min() and images.max() <= 1
    assert labels.shape == (2,)
    assert labels.dtype == torch.int64
    assert labels.min() >= 0 and labels.max() <= 9
    assert Generator()(torch.randn(2, 100), labels).shape == images.shape
    assert Discriminator()(images, labels).shape == (2, 1)
    assert not test_loader.drop_last


def test_get_dataloaders_rejects_invalid_batch_size(fake_torchvision):
    with pytest.raises(ValueError):
        get_dataloaders(batch_size=0)


def test_get_dataloaders_rejects_negative_num_workers(fake_torchvision):
    with pytest.raises(ValueError):
        get_dataloaders(num_workers=-1)


def test_get_dataloaders_seed_reproduces_shuffle(fake_torchvision):
    def order(loader):
        return torch.cat([images.view(images.shape[0], -1) for images, _ in loader])

    train_a, _ = get_dataloaders(batch_size=1, seed=7)
    train_b, _ = get_dataloaders(batch_size=1, seed=7)
    train_c, _ = get_dataloaders(batch_size=1, seed=8)

    assert torch.equal(order(train_a), order(train_b))
    assert not torch.equal(order(train_a), order(train_c))
