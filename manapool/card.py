UNKNOWN = object()


class Card:
    """Represents a MtG card. The only required attribute is the title.

    Cards are immutable. Clone with new values if you need to change an attribute.
    """

    def __init__(self, title: str):
        """
        :param title: The title of the card. Is converted to a str, but the value may not be the
            empty string. May not be None.

        :raises ValueError:
        """
        if title is None:
            raise ValueError("None is not accepted as a title.")
        title = str(title)
        if title == "":
            raise ValueError("Empty string.")
        self._title = title

    @property
    def title(self) -> str:
        return self._title
