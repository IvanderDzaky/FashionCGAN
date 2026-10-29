import json

import pytest
import torch
from torch.utils.data import DataLoader, TensorDataset

from fashion_cgan.evaluate import (
    Classifier,
    classifier_accuracy,
    evaluate,
    generated_class_accuracy,
    train_classifier,
)
from fashion_cgan.models import Generator


def test_classifier_outputs_one_logit_per_class():
    classifier = Classifier()

    logits = classifier(torch.randn(2, 1, 28, 28))

    assert logits.shape == (2, 10)
    with pytest.raises(ValueError):
        classifier(torch.randn(2, 28, 28))


def test_train_classifier_and_accuracy_on_separable_data():
    images = torch.randn(20, 1, 28, 28)
    labels = torch.arange(20) % 10
    loader = DataLoader(TensorDataset(images, labels), batch_size=10)

    classifier = train_classifier(loader, epochs=1)
    accuracy = classifier_accuracy(classifier, loader)

    assert 0.0 <= accuracy <= 1.0
    with pytest.raises(ValueError):
        train_classifier(loader, epochs=0)


def test_classifier_accuracy_rejects_empty_loader():
    empty = DataLoader(TensorDataset(torch.empty(0, 1, 28, 28), torch.empty(0, dtype=torch.long)))
    with pytest.raises(ValueError):
        classifier_accuracy(Classifier(), empty)


def test_generated_class_accuracy_reports_each_requested_class():
    result = generated_class_accuracy(Classifier(), Generator(), [0, 3], samples_per_class=2, seed=7)

    assert list(result) == ["T-shirt/top", "Dress"]
    assert all(item["samples"] == 2 for item in result.values())
    assert all(0.0 <= item["accuracy"] <= 1.0 for item in result.values())
    with pytest.raises(ValueError):
        generated_class_accuracy(Classifier(), Generator(), [])
    with pytest.raises(ValueError):
        generated_class_accuracy(Classifier(), Generator(), [10])


def test_evaluate_writes_json_and_csv(tmp_path, monkeypatch):
    images = torch.rand(10, 1, 28, 28).mul(2).sub(1)
    loader = DataLoader(TensorDataset(images, torch.arange(10) % 10), batch_size=5)
    monkeypatch.setattr("fashion_cgan.data.get_dataloaders", lambda *args, **kwargs: (loader, loader))
    config = {
        "seed": 42,
        "data": {"root": str(tmp_path), "classes": 10},
        "model": {"latent_dim": 100},
        "training": {"batch_size": 5},
    }
    checkpoint_path = tmp_path / "checkpoint.pt"
    torch.save({"epoch": 1, "generator": Generator().state_dict(), "config": config}, checkpoint_path)

    report = evaluate(checkpoint_path, tmp_path / "evaluation", epochs=1, samples_per_class=2, device="cpu")

    assert 0.0 <= report["real_accuracy"] <= 1.0
    assert len(report["generated"]) == 10
    saved = json.loads((tmp_path / "evaluation" / "evaluation.json").read_text(encoding="utf-8"))
    assert saved["generated_accuracy_mean"] == report["generated_accuracy_mean"]
    assert len((tmp_path / "evaluation" / "evaluation.csv").read_text(encoding="utf-8").splitlines()) == 11
