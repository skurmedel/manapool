from typing import Union


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
