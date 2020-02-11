from abc import abstractmethod
from typing import Sequence, Tuple

from card import Card


class Deck(Tuple[Card]):
    """Represents a Deck. Decks are immutable."""

    def __new__(cls, *args: Card):
        """
        Creates a new deck from the given cards.
        :param args: A sequence of cards.

        :raises ValueError:
        """

        def is_not_a_card(c):
            return not isinstance(c, Card)

        if any(is_not_a_card(c) for c in args):
            raise ValueError("An item of cards was not of a Card type.")
        return super(Deck, cls).__new__(cls, tuple(args))

    @property
    def empty(self) -> bool:
        return len(self) == 0
