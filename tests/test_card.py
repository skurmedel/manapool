import pytest
from manapool.card import Card


def test_card_title_required():
    with pytest.raises(ValueError):
        Card(None)
    with pytest.raises(ValueError):
        Card("")


def test_card_title_str_converts():
    c = Card(1)
    assert (c.title == "1")

    class Dummy:
        def __str__(self):
            return ""

    with pytest.raises(ValueError):
        Card(Dummy())
