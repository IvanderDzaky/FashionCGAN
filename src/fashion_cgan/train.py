"""Train the Fashion-MNIST conditional GAN."""

import argparse
import csv
import random
from pathlib import Path

import torch
import yaml
from torch import nn

from fashion_cgan.data import get_dataloaders
from fashion_cgan.models import Discriminator, Generator


def train(
    config_path: str | Path = "configs/default.yaml",
    epochs: int | None = None,
    max_batches: int | None = None,
    device: str | torch.device | None = None,
    download: bool = True,
) -> list[dict[str, float | int]]:
    """Train both models; save per-epoch checkpoints and CSV metrics."""
    with Path(config_path).open(encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)

    seed = config["seed"]
    random.seed(seed)
    torch.manual_seed(seed)
    data_config, model_config, training_config = config["data"], config["model"], config["training"]
    device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    train_loader, _ = get_dataloaders(data_config["root"], training_config["batch_size"], download)

    generator = Generator(model_config["latent_dim"], data_config["classes"]).to(device)
    discriminator = Discriminator(data_config["classes"]).to(device)
    betas = tuple(training_config["betas"])
    generator_optimizer = torch.optim.Adam(generator.parameters(), lr=training_config["learning_rate"], betas=betas)
    discriminator_optimizer = torch.optim.Adam(
        discriminator.parameters(), lr=training_config["learning_rate"], betas=betas
    )
    criterion = nn.BCEWithLogitsLoss()
    output_dir = Path(training_config.get("output_dir", "outputs"))
    output_dir.mkdir(parents=True, exist_ok=True)
    history: list[dict[str, float | int]] = []
    epoch_count = epochs if epochs is not None else training_config["epochs"]

    for epoch in range(1, epoch_count + 1):
        generator.train()
        discriminator.train()
        d_loss_sum = g_loss_sum = 0.0
        batches = 0
        for images, labels in train_loader:
            if max_batches is not None and batches >= max_batches:
                break
            images, labels = images.to(device), labels.to(device, dtype=torch.long)
            batch_size = images.shape[0]

            discriminator_optimizer.zero_grad(set_to_none=True)
            real_logits = discriminator(images, labels)
            noise = torch.randn(batch_size, model_config["latent_dim"], device=device)
            fake_images = generator(noise, labels)
            fake_logits = discriminator(fake_images.detach(), labels)
            d_loss = criterion(real_logits, torch.ones_like(real_logits)) + criterion(
                fake_logits, torch.zeros_like(fake_logits)
            )
            d_loss.backward()
            discriminator_optimizer.step()

            discriminator_optimizer.zero_grad(set_to_none=True)
            for parameter in discriminator.parameters():
                parameter.requires_grad_(False)
            generator_optimizer.zero_grad(set_to_none=True)
            generated_logits = discriminator(fake_images, labels)
            g_loss = criterion(generated_logits, torch.ones_like(generated_logits))
            g_loss.backward()
            generator_optimizer.step()
            for parameter in discriminator.parameters():
                parameter.requires_grad_(True)

            d_loss_sum += d_loss.item()
            g_loss_sum += g_loss.item()
            batches += 1

        if not batches:
            raise ValueError("training loader produced no batches")
        metrics = {"epoch": epoch, "discriminator_loss": d_loss_sum / batches, "generator_loss": g_loss_sum / batches}
        history.append(metrics)
        torch.save(
            {
                "epoch": epoch,
                "generator": generator.state_dict(),
                "discriminator": discriminator.state_dict(),
                "generator_optimizer": generator_optimizer.state_dict(),
                "discriminator_optimizer": discriminator_optimizer.state_dict(),
                "config": config,
            },
            output_dir / f"cgan_epoch_{epoch}.pt",
        )
        with (output_dir / "metrics.csv").open("w", newline="", encoding="utf-8") as metrics_file:
            writer = csv.DictWriter(metrics_file, fieldnames=metrics)
            writer.writeheader()
            writer.writerows(history)

    return history


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--epochs", type=int)
    parser.add_argument("--max-batches", type=int, help="Limit batches per epoch for a smoke run")
    parser.add_argument("--device")
    args = parser.parse_args()
    history = train(args.config, epochs=args.epochs, max_batches=args.max_batches, device=args.device)
    print(f"Training complete: {len(history)} epoch(s); latest metrics: {history[-1]}")


if __name__ == "__main__":
    main()
