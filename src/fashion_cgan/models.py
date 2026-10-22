"""MLP models for the Fashion-MNIST conditional GAN."""

import torch
from torch import nn
from torch.nn import functional as F


class Generator(nn.Module):
    """Generate 28x28 grayscale images from noise and class labels."""

    def __init__(self, latent_dim: int = 100, num_classes: int = 10) -> None:
        super().__init__()
        self.latent_dim = latent_dim
        self.num_classes = num_classes
        self.network = nn.Sequential(
            nn.Linear(latent_dim + num_classes, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 512),
            nn.ReLU(inplace=True),
            nn.Linear(512, 28 * 28),
            nn.Tanh(),
        )

    def forward(self, noise: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        if not isinstance(noise, torch.Tensor) or noise.ndim != 2 or noise.shape[1] != self.latent_dim:
            raise ValueError(f"noise must have shape [B, {self.latent_dim}]")
        _validate_labels(labels, noise.shape[0], noise.device, self.num_classes)
        conditioned = torch.cat((noise, F.one_hot(labels.to(torch.long), self.num_classes).to(noise.dtype)), dim=1)
        return self.network(conditioned).view(noise.shape[0], 1, 28, 28)


class Discriminator(nn.Module):
    """Score grayscale images conditioned on class labels; returns logits."""

    def __init__(self, num_classes: int = 10) -> None:
        super().__init__()
        self.num_classes = num_classes
        self.network = nn.Sequential(
            nn.Linear(28 * 28 + num_classes, 512),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 1),
        )

    def forward(self, images: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
        if images.ndim != 4 or tuple(images.shape[1:]) != (1, 28, 28):
            raise ValueError("images must have shape [B, 1, 28, 28]")
        _validate_labels(labels, images.shape[0], images.device, self.num_classes)
        conditioned = torch.cat(
            (images.flatten(start_dim=1), F.one_hot(labels.to(torch.long), self.num_classes).to(images.dtype)), dim=1
        )
        return self.network(conditioned)


def _validate_labels(labels: torch.Tensor, batch_size: int | None, device: torch.device, num_classes: int) -> None:
    if not isinstance(labels, torch.Tensor) or labels.ndim != 1:
        raise ValueError("labels must be a rank-1 integer tensor")
    if batch_size is not None and labels.shape[0] != batch_size:
        raise ValueError("labels and inputs must have the same batch size")
    if labels.device != device:
        raise ValueError("labels and inputs must be on the same device")
    if labels.dtype not in (torch.uint8, torch.int8, torch.int16, torch.int32, torch.int64):
        raise ValueError("labels must use an integer dtype")
    if torch.any((labels < 0) | (labels >= num_classes)).item():
        raise ValueError(f"labels must be in the range 0..{num_classes - 1}")
