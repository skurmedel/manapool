from typing import Union, Mapping
from enum import Enum, unique


class _Singleton(type):
    instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


class Unknown(metaclass=_Singleton):
    """Represents an Unknown value."""

    def __str__(self):
        return "<Unknown>"

    def __repr__(self):
        return "<Unknown>"


UNKNOWN = Unknown()


class Card:
    """Represents a MtG card. The only required attribute is the title.

    Cards are immutable. Clone with new values if you need to change an attribute.
    """

    def __init__(self, title: str, mvid: Union[Unknown, int] = UNKNOWN):
        """
        :param title: The title of the card. Is converted to a str, but the value may not be the
            empty string. May not be None.
        :param mvid: The multiverse id. Assigned by Wizards of the Coast. Uniquely identifies a card.

        :raises ValueError:
        """
        if title is None:
            raise ValueError("None is not accepted as a title.")
        title = str(title)
        if title == "":
            raise ValueError("Empty string.")
        self._title = title

        if isinstance(mvid, Unknown):
            self._mvid = mvid
        else:
            self._mvid = int(mvid)

    @property
    def title(self) -> str:
        return self._title

    @property
    def mvid(self) -> Union[Unknown, int]:
        """The multiverse ID."""
        return self._mvid


@unique
class Colour(Enum):
    """Represents a mana colour. It also contains the Colourless and Generic pseudo-colours. """

    Less = 0
    Generic = 1
    White = 2
    Blue = 3
    Black = 4
    Green = 5
    Red = 6

    @classmethod
    def pure(cls):
        """Returns the WUBGR colours, not any of the pseudo-colours."""
        return [Colour.White, Colour.Blue, Colour.Black, Colour.Green, Colour.Red]


class ManaCost:
    """Represents a mana cost. Can only deal with integer costs. This object acts immutably."""
    __slots__ = ["_colours", "_converted"]

    def __init__(self, values: Union[Mapping[Colour, int]] = {}):
        """
        :param values:
            May be one of the following:
                Mapping[Colour, int] - the cost for the present values is set to the positive associated integer, all
                other colours are zero cost.
        """
        self._colours = [0] * len(Colour)
        if values is None:
            raise ValueError("None is not an accepted value.")
        for k,v in values.items():
            if not isinstance(v, int):
                raise ValueError("non integer argument.")
            if v < 0:
                raise ValueError("Negative cost.")
            self._colours[k.value] = v

    def __getitem__(self, item: Colour) -> int:
        """Retrieves the cost for the given colour."""
        if not isinstance(item, Colour):
            raise ValueError("Expected an enum value of Colour.")
        return self._colours[item.value]

    @property
    def converted(self) -> int:
        """Returns the converted mana cost (CMC). It's the sum of the costs of each individual colour."""
        return sum(self._colours)

    @property
    def less(self) -> int:
        return self[Colour.Less]

    @property
    def generic(self) -> int:
        return self[Colour.Generic]

    @property
    def white(self) -> int:
        return self[Colour.White]

    @property
    def blue(self) -> int:
        return self[Colour.Blue]

    @property
    def black(self) -> int:
        return self[Colour.Black]

    @property
    def green(self) -> int:
        return self[Colour.Green]

    @property
    def red(self) -> int:
        return self[Colour.Red]
