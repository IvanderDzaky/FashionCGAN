import pytest
import torch

from fashion_cgan.models import Discriminator, Generator


@pytest.mark.parametrize("batch_size", [1, 4])
def test_generator_shape_and_range(batch_size):
    model = Generator()
    images = model(torch.randn(batch_size, 100), torch.arange(batch_size) % 10)

    assert images.shape == (batch_size, 1, 28, 28)
    assert torch.isfinite(images).all()
    assert images.min() >= -1 and images.max() <= 1


@pytest.mark.parametrize("batch_size", [1, 4])
def test_discriminator_returns_one_finite_logit_per_image(batch_size):
    model = Discriminator()
    logits = model(torch.randn(batch_size, 1, 28, 28), torch.arange(batch_size) % 10)

    assert logits.shape == (batch_size, 1)
    assert torch.isfinite(logits).all()


def test_both_models_use_label_conditioning():
    generator = Generator()
    discriminator = Discriminator()
    with torch.no_grad():
        for model in (generator, discriminator):
            for parameter in model.parameters():
                parameter.zero_()
            model.network[0].weight[0, -10] = 1
            model.network[0].bias[0] = -0.5
            model.network[2].weight[0, 0] = 1
            model.network[2].bias[0] = 0.5
            model.network[4].weight[0, 0] = 1
        generator.network[-2].weight[0, 0] = 1
        discriminator.network[-1].weight[0, 0] = 1

    noise = torch.zeros(1, 100)
    image = torch.zeros(1, 1, 28, 28)
    generated_zero = generator(noise, torch.tensor([0]))
    generated_one = generator(noise, torch.tensor([1]))
    score_zero = discriminator(image, torch.tensor([0]))
    score_one = discriminator(image, torch.tensor([1]))

    assert not torch.equal(generated_zero, generated_one)
    assert not torch.equal(score_zero, score_one)


def test_models_accept_integer_label_dtypes():
    labels = torch.tensor([1, 4], dtype=torch.int32)

    assert Generator()(torch.randn(2, 100), labels).shape == (2, 1, 28, 28)
    assert Discriminator()(torch.randn(2, 1, 28, 28), labels).shape == (2, 1)


@pytest.mark.parametrize("model_kind", ["generator", "discriminator"])
def test_models_have_finite_nonzero_parameter_gradients(model_kind):
    if model_kind == "generator":
        model = Generator()
        output = model(torch.randn(3, 100), torch.tensor([1, 4, 8]))
    else:
        model = Discriminator()
        output = model(torch.randn(3, 1, 28, 28), torch.tensor([1, 4, 8]))
    output.square().mean().backward()

    gradients = [parameter.grad for parameter in model.parameters() if parameter.requires_grad]
    assert all(gradient is not None and torch.isfinite(gradient).all() for gradient in gradients)
    assert any(torch.count_nonzero(gradient) for gradient in gradients)


@pytest.mark.parametrize(
    ("noise", "labels", "message"),
    [
        (torch.randn(2, 99), torch.tensor([0, 1]), "noise must have shape"),
        (torch.randn(2, 100), torch.tensor([0]), "same batch size"),
        (torch.randn(2, 100), torch.tensor([0, 10]), "range"),
        (torch.randn(2, 100), torch.tensor([0.0, 1.0]), "integer dtype"),
    ],
)
def test_generator_rejects_invalid_inputs(noise, labels, message):
    with pytest.raises(ValueError, match=message):
        Generator()(noise, labels)


@pytest.mark.parametrize(
    ("images", "labels", "message"),
    [
        (torch.randn(2, 28, 28), torch.tensor([0, 1]), "images must have shape"),
        (torch.randn(2, 1, 28, 28), torch.tensor([0]), "same batch size"),
        (torch.randn(2, 1, 28, 28), torch.tensor([-1, 1]), "range"),
        (torch.randn(2, 1, 28, 28), torch.tensor([0.0, 1.0]), "integer dtype"),
    ],
)
def test_discriminator_rejects_invalid_inputs(images, labels, message):
    with pytest.raises(ValueError, match=message):
        Discriminator()(images, labels)
