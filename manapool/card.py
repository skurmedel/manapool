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
        colours = [0] * len(Colour)
        if values is None:
            raise ValueError("None is not an accepted value.")
        for k, v in values.items():
            if not isinstance(v, int):
                raise ValueError("non integer argument.")
            if v < 0:
                raise ValueError("Negative cost.")
            colours[k.value] = v

        self._colours = tuple(colours)
        self._converted = sum(self._colours)

    def __getitem__(self, item: Colour) -> int:
        """Retrieves the cost for the given colour."""
        if not isinstance(item, Colour):
            raise ValueError("Expected an enum value of Colour.")
        return self._colours[item.value]

    @property
    def converted(self) -> int:
        """Returns the converted mana cost (CMC). It's the sum of the costs of each individual colour."""
        return self._converted

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

    def __eq__(self, other):
        if not isinstance(other, ManaCost):
            return False

        return self._colours == other._colours

    def __hash__(self):
        return hash(self._colours)


class Card:
    """Represents a MtG card. The only required attribute is the title.

    Cards are immutable. Clone with new values if you need to change an attribute.

    The Card type is simplistic by choice. If you need to encode a richer set of data, simply subclass the Card type.

    The Card type is also not supposed to check that the Card is legal or even exists, that's up to the user. Most
    likely the data will be read from an API (that's why we provide the multiverse id field.) Magic the Gathering is
    simply too flexible and vast for that to be practical. For example w allow for Cards that may not make sense, like a
    basic land with a mana cost.

    Most of the functions in manapool are designed to work with Card, since the data it encodes is enough for a great
    deal of statistics and probabilities calculations pertinent to Magic the Gathering.
    """

    def __init__(self, title: str, cost: Union[Unknown, ManaCost] = UNKNOWN, mvid: Union[Unknown, int] = UNKNOWN):
        """
        :param title: The title of the card. Is converted to a str, but the value may not be the
            empty string. May not be None.
        :param cost: The mana cost.
        :param mvid: The multiverse id. Assigned by Wizards of the Coast. Uniquely identifies a card.

        :raises ValueError:
        """
        if title is None:
            raise ValueError("None is not accepted as a title.")
        title = str(title)
        if title == "":
            raise ValueError("Empty string.")
        self._title = title

        if isinstance(cost, Unknown) or isinstance(cost, ManaCost):
            self._cost = cost
        else:
            raise ValueError("Expected cost to be either UNKNOWN or a ManaCost.")

        if isinstance(mvid, Unknown):
            self._mvid = mvid
        else:
            self._mvid = int(mvid)

    @property
    def title(self) -> str:
        return self._title

    @property
    def cost(self) -> Union[Unknown, ManaCost]:
        return self._cost

    @property
    def mvid(self) -> Union[Unknown, int]:
        """The multiverse ID."""
        return self._mvid

    def __eq__(self, other):
        """Compares two Card instances. Each attribute in self is tested against it's sibling in other.

        Notably if an attribute is UNKNOWN it is only equal if both are UNKNOWN.
        """
        if not isinstance(other, Card):
            return False
        return self.title == other.title and self.cost == other.cost and self.mvid == other.mvid

    def __hash__(self):
        return hash((self.title, self.cost, self.mvid))