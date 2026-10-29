import pytest
import torch

from fashion_cgan.utils import (
    FASHION_MNIST_CLASSES,
    class_names,
    denormalize,
    load_metrics,
    save_image_grid,
)


def test_denormalize_maps_range_to_unit_interval():
    images = torch.tensor([[-1.5, -1.0, 0.0, 1.0, 1.5]])

    result = denormalize(images)

    assert torch.allclose(result, torch.tensor([[0.0, 0.0, 0.5, 1.0, 1.0]]))


def test_denormalize_rejects_non_tensor():
    with pytest.raises(TypeError):
        denormalize([[0.0]])


def test_class_names_maps_indices_and_rejects_out_of_range():
    assert class_names([0, 9]) == [FASHION_MNIST_CLASSES[0], FASHION_MNIST_CLASSES[9]]
    with pytest.raises(ValueError):
        class_names([10])


def test_load_metrics_reads_typed_rows(tmp_path):
    path = tmp_path / "metrics.csv"
    path.write_text(
        "epoch,discriminator_loss,generator_loss\n1,0.36,3.27\n2,0.33,5.03\n", encoding="utf-8"
    )

    rows = load_metrics(path)

    assert rows == [
        {"epoch": 1, "discriminator_loss": 0.36, "generator_loss": 3.27},
        {"epoch": 2, "discriminator_loss": 0.33, "generator_loss": 5.03},
    ]


def test_save_image_grid_writes_png_and_labels(tmp_path):
    images = torch.rand(4, 1, 28, 28).mul(2).sub(1)

    output = save_image_grid(images, tmp_path / "grid.png", labels=[0, 1, 2, 3], nrow=2)

    assert output.is_file()
    assert (tmp_path / "grid.labels.txt").read_text(encoding="utf-8").split() == ["0", "1", "2", "3"]
