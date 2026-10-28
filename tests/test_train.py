import csv

import torch
import yaml
from torch.utils.data import DataLoader, TensorDataset

from fashion_cgan.models import Discriminator, Generator
from fashion_cgan.train import train


def test_training_resumes_from_checkpoint_at_next_epoch(tmp_path, monkeypatch):
    images = torch.rand(2, 1, 28, 28).mul(2).sub(1)
    labels = torch.tensor([1, 3])
    loader = DataLoader(TensorDataset(images, labels), batch_size=2)
    monkeypatch.setattr("fashion_cgan.train.get_dataloaders", lambda *args, **kwargs: (loader, loader))
    config = {
        "seed": 42,
        "data": {"root": str(tmp_path), "classes": 10},
        "model": {"latent_dim": 100},
        "training": {
            "batch_size": 2,
            "learning_rate": 0.0002,
            "betas": [0.5, 0.999],
            "epochs": 1,
            "output_dir": str(tmp_path / "outputs"),
        },
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

    train(config_path, device="cpu")
    history = train(config_path, device="cpu", resume=tmp_path / "outputs" / "cgan_epoch_1.pt")

    assert history[0]["epoch"] == 2
    assert all(torch.isfinite(torch.tensor(value)) for value in history[0].values())
    assert (tmp_path / "outputs" / "cgan_epoch_2.pt").is_file()


def test_training_saves_metrics_and_loadable_checkpoint(tmp_path, monkeypatch):
    images = torch.rand(2, 1, 28, 28).mul(2).sub(1)
    labels = torch.tensor([1, 3])
    loader = DataLoader(TensorDataset(images, labels), batch_size=2)
    monkeypatch.setattr("fashion_cgan.train.get_dataloaders", lambda *args, **kwargs: (loader, loader))
    config = {
        "seed": 42,
        "data": {"root": str(tmp_path), "classes": 10},
        "model": {"latent_dim": 100},
        "training": {
            "batch_size": 2,
            "learning_rate": 0.0002,
            "betas": [0.5, 0.999],
            "epochs": 1,
            "output_dir": str(tmp_path / "outputs"),
        },
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.safe_dump(config), encoding="utf-8")

    history = train(config_path, device="cpu")

    assert len(history) == 1
    assert all(torch.isfinite(torch.tensor(value)) for value in history[0].values())
    assert history[0]["epoch"] == 1
    checkpoint_path = tmp_path / "outputs" / "cgan_epoch_1.pt"
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    generator, discriminator = Generator(), Discriminator()
    generator.load_state_dict(checkpoint["generator"])
    discriminator.load_state_dict(checkpoint["discriminator"])
    with (tmp_path / "outputs" / "metrics.csv").open(encoding="utf-8", newline="") as metrics_file:
        rows = list(csv.DictReader(metrics_file))
    assert len(rows) == 1
    assert int(rows[0]["epoch"]) == 1
