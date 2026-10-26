import pytest
import torch
from PIL import Image

from fashion_cgan.generate import generate_grid
from fashion_cgan.models import Generator


def test_generate_grid_loads_checkpoint_and_saves_png(tmp_path):
    generator = Generator()
    checkpoint_path = tmp_path / "checkpoint.pt"
    torch.save(
        {
            "generator": generator.state_dict(),
            "config": {"model": {"latent_dim": 100}, "data": {"classes": 10}},
        },
        checkpoint_path,
    )
    output_path = tmp_path / "images" / "grid.png"

    result = generate_grid(checkpoint_path, [0, 3, 9], output_path, device="cpu")

    assert result == output_path
    with Image.open(output_path) as image:
        assert image.format == "PNG"
        assert image.size == (3 * 28 + 4 * 2, 28 + 2 * 2)


@pytest.mark.parametrize("labels", [[], [10], [-1]])
def test_generate_grid_rejects_invalid_labels(tmp_path, labels):
    checkpoint_path = tmp_path / "checkpoint.pt"
    torch.save(
        {
            "generator": Generator().state_dict(),
            "config": {"model": {"latent_dim": 100}, "data": {"classes": 10}},
        },
        checkpoint_path,
    )
    with pytest.raises(ValueError):
        generate_grid(checkpoint_path, labels, tmp_path / "grid.png", device="cpu")
