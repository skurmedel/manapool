from typing import Union, Mapping
from enum import Flag, auto, unique


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
class Color(Flag):
    """Represents a mana colour. It also contains the Colourless and Generic pseudo-colours.

    Mainly used to specify mana costs.

    .. note::
        According to the MtG rules (as of feb 2020), "colorless is not a color". But there have been a set with colorless
        mana costs.

        The colours are:
            white, blue, black, green, red (wubgr)

        We allow for this inconsistency with the rules in the name of flexibility. Generic is not a colour either but
        likewise, it's useful to treat it as one for mana cost reasons.

    """

    White = 1
    Blue = 2
    Black = 4
    Green = 8
    Red = 16
    Less = 32
    Generic = 64

    @classmethod
    def pure(cls):
        """Returns the WUBGR colours, not any of the pseudo-colours."""
        return [Color.White, Color.Blue, Color.Black, Color.Green, Color.Red]


def _parse_mana_cost(s: str):
    NEXT = 0
    ENTERED_PART = 1
    EXITING_PART = 2

    pure_mapping = {
        "W": Color.White,
        "w": Color.White,
        "U": Color.Blue,
        "u": Color.Blue,
        "B": Color.Black,
        "b": Color.Black,
        "G": Color.Green,
        "g": Color.Green,
        "R": Color.Red,
        "r": Color.Red
    }
    generic_mapping = {
        str(i): i for i in range(0, 10)
    }

    colours = {}
    converted = 0

    state = NEXT
    for c in s:
        if state == ENTERED_PART:
            if c in "WUBGRwubgrX0123456789":
                if c in pure_mapping:
                    color = pure_mapping[c]
                    if color in colours:
                        colours[pure_mapping[c]] = colours[pure_mapping[c]] + 1
                    else:
                        colours[pure_mapping[c]] = 1
                    converted += 1
                elif c in "0123456789":
                    value = generic_mapping[c]
                    if Color.Generic not in colours:
                        colours[Color.Generic] = 0
                    colours[Color.Generic] = colours[Color.Generic] + value
                    converted += value
                state = EXITING_PART
            else:
                raise ValueError("Encountered unexpected symbol: {}".format(c))
        elif state == EXITING_PART:
            if c != "}":
                raise ValueError("Expected closing }.")
            state = NEXT
        elif c == "{":
            state = ENTERED_PART
        else:
            raise ValueError("Encountered unexpected symbol: {}".format(c))

    if state != NEXT:
        raise ValueError("Unmatched { or }.")

    return colours, converted


class ManaCost:
    """Represents a mana cost. Can only deal with integer costs. This object acts immutably.

    .. note::
        Technically a card can have no cost at all (not even zero) and thus can not be played by normal means.

        This object can not represent such a "non-cost".

    .. note::
        At the moment, a cost with moncolored hybrid mana can't be expressed. Phyraxian costs are not supported either.

    .. note::
        Can not express X generic mana in a cost at the moment.
    """
    __slots__ = ["_colours", "_converted", "_hash"]

    def __init__(self, values: Union[Mapping[Color, int], str] = {}):
        """
        values may be one of the following:

        Mapping[Colour, int]:
        the cost for the present values is set to the positive associated integer, all other colours are zero cost.

        str:
        A string of the following format:

            part    = "{" [WUBGRwubgr0-9] "}"
            cost    = part+

        Each letter represents a colour, and a digit represents an amount of generic mana.
        After parsing, the number of parts for each colour is summed.

        Thus, to say 2 white mana and 3 generic, we pass the string "{W}{W}{3}". You might also say "{W}{W}{1}{2}" etc.
        To say 1 blue, 1 red, 1 generic, we pass "{U}{R}{1}".
        """
        colours = {}
        self._converted = 0
        if values is None:
            raise ValueError("None is not an accepted value.")
        if isinstance(values, str):
            colours, self._converted = _parse_mana_cost(values)
        else:
            for k, v in values.items():
                if not isinstance(v, int):
                    raise ValueError("non integer argument.")
                if v < 0:
                    raise ValueError("Negative cost.")
                colours[k] = v
                self._converted += v

        self._colours = colours
        self._hash = hash(tuple(self._colours))

    def __getitem__(self, item: Color) -> int:
        """Retrieves the cost for the given colour or hybrid, only the exact combination is counted.

        For example: given a cost {W/B}{W} and you do cost[Color.White] you will get 1 back.

            >>> c = ManaCost({Color.White | Color.Black: 1, Color.White: 1})
            >>> c[Color.White]
            1
        """
        if not isinstance(item, Color):
            raise ValueError("Expected an flag value of Colour.")
        return self._colours.get(item, 0)

    def total(self, c: Color) -> int:
        """Retrieves the sum of all the costs with the given colour, hybrids included.

            >>> c = ManaCost({Color.White | Color.Red: 1, Color.White: 1, Color.Generic: 2})
            >>> c.total(Color.White)
            2
        """
        if not isinstance(c, Color):
            raise ValueError("Expected a Color flag.")
        t = 0
        for k in self._colours:
            if c in k:
                t += self._colours[k]
        return t

    @property
    def converted(self) -> int:
        """Returns the converted mana cost (CMC). It's the sum of the costs of each individual colour."""
        return self._converted

    @property
    def less(self) -> int:
        return self[Color.Less]

    @property
    def generic(self) -> int:
        """Count of cards white a White colour. This counts hybrid costs as well."""
        return self.total(Color.Generic)

    @property
    def white(self) -> int:
        """White colour cost. This counts hybrid costs as well."""
        return self.total(Color.White)

    @property
    def blue(self) -> int:
        """Blue colour cost. This counts hybrid costs as well."""
        return self.total(Color.Blue)

    @property
    def black(self) -> int:
        """Black colour cost. This counts hybrid costs as well."""
        return self.total(Color.Black)

    @property
    def green(self) -> int:
        """Green colour cost. This counts hybrid costs as well."""
        return self.total(Color.Green)

    @property
    def red(self) -> int:
        """Red colour cost. This counts hybrid costs as well."""
        return self.total(Color.Red)

    def __eq__(self, other):
        if not isinstance(other, ManaCost):
            return False

        return self._colours == other._colours

    def __hash__(self):
        return self._hash

    def __repr__(self):
        """Prints the card in a format suitable for the constructor of ManaCost."""
        pure_mapping = {
            Color.White: "{W}",
            Color.Blue: "{U}",
            Color.Black: "{B}",
            Color.Green: "{G}",
            Color.Red: "{R}",
        }

        parts = []
        if self.converted == 0:
            parts = ["{0}"]
        else:
            for c in Color:
                if c is Color.Generic:
                    val = self[c]
                    if val > 0:
                        parts.extend(["{", str(val), "}"])
                elif c is Color.Less:
                    parts.extend("{C}" * self[c])
                else:
                    parts.extend(pure_mapping[c] * self[c])

        return "".join(parts)


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
