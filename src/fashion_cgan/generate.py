"""Generate labeled Fashion-MNIST image grids from a training checkpoint."""

import argparse
from pathlib import Path
from collections.abc import Sequence

import torch

from fashion_cgan.models import Generator


def generate_grid(
    checkpoint_path: str | Path,
    labels: Sequence[int],
    output_path: str | Path = "outputs/generated_grid.png",
    device: str | torch.device | None = None,
    seed: int = 42,
) -> Path:
    """Generate one image per label and save them as a PNG grid."""
    if not labels:
        raise ValueError("at least one label is required")
    device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
    config = checkpoint["config"]
    latent_dim, num_classes = config["model"]["latent_dim"], config["data"]["classes"]
    label_tensor = torch.tensor(labels, dtype=torch.long, device=device)
    if torch.any((label_tensor < 0) | (label_tensor >= num_classes)).item():
        raise ValueError(f"labels must be in the range 0..{num_classes - 1}")

    generator = Generator(latent_dim, num_classes).to(device)
    generator.load_state_dict(checkpoint["generator"])
    generator.eval()
    generator_device_rng = torch.Generator(device=device).manual_seed(seed)
    noise = torch.randn(len(labels), latent_dim, generator=generator_device_rng, device=device)
    with torch.inference_mode():
        images = generator(noise, label_tensor).cpu()

    from torchvision.utils import save_image

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    save_image(images, output_path, nrow=min(len(labels), 10), normalize=True, value_range=(-1, 1))
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", nargs="?", default="outputs/cgan_epoch_1.pt")
    parser.add_argument("--labels", type=int, nargs="+", default=list(range(10)))
    parser.add_argument("--output", default="outputs/generated_grid.png")
    parser.add_argument("--device")
    args = parser.parse_args()
    print(generate_grid(args.checkpoint, args.labels, args.output, args.device))


if __name__ == "__main__":
    main()
