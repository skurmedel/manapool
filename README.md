# manapool

![Python package](https://github.com/skurmedel/manapool/workflows/Python%20package/badge.svg)

manapool is a Python library for doing Magic the Gathering calculations. The focus is on Deck statistics and probabilities.

An example of a typical calculations may be to list a deck's mana curve, or the chance that your opening hand contains a certain card.

At the moment it's in the design stage.

## Design philosophy

manapool's primary focus is on doing calculations. manapool is not a database for cards. It may in many cases allow MtG 
cards that don't exist or are against the rules. If you wanna look up existing cards, Scryfall is excellent, and if 
you want a database, there's Delver Lens and a myriad of alternatives.

Some use cases for manapool:
 - quickly finding the mana curve of a deck and plotting it
 - tallying a deck (i.e counts of cards)
 - counts of types in a deck
 - opening hands
 - probability that you draw a card after X draws
 
 As you can see, many of these use cases really need very little card data. A title (which can be bogus), mana cost and
 type is enough for a great deal of valuable statistics. In case of probabilities you often need only the title.
 
 To this end manapool should strive to:
 - use simple, mostly immutable types that do "enough".
 - use types that make it hard for the user to do mistakes 
 - be non-ambiguous
 - be pedantic about types, see two previous points
 - flat type hierarchies
 - allow for easy bulk operations on decks.
 - most operations are performed with simple composable functions, not methods.
 
### Examples

#### Opening hand

```python
from manapool.deck import Card, Deck, opening_hand

decklist = [
    (4, "Bonecrusher Giant"),
    (4, "Cavalier of Flame"),
    (2, "Cavalier of Gales"),
    (2, "Dream Trawler"),
    (3, "Kenrith, the Returned King"),
    (4, "Sphinx of Foresight"),
    (2, "Aether Gust"),
    (3, "Deafening Clarion"),
    (1, "Shimmer of Possibility"),
    (4, "Fires of Invention"),
    (4, "Teferi, Time Raveler"),
    (2, "Castle Vantress"),
    (3, "Fabled Passage"),
    (4, "Hallowed Fountain"),
    (2, "Island"),
    (2, "Mountain"),
    (1, "Plains"),
    (3, "Sacred Foundry"),
    (4, "Steam Vents"),
    (3, "Temple of Epiphany"),
    (3, "Temple of Triumph"),
]


def cardify(values):
    for count, title in values:
        yield count, Card(title)


deck = Deck(*cardify(decklist))

first_hand = opening_hand(deck)
```

### Coding style
 
 - PEP8
 - use python type annotations, they do wonders for completion and documentation.
 - try to describe the interface in the doc, test the interface.
 - group operations in modules, for example deck.tally takes a Deck.


### Limitations

- does not support Phyraxian costs (where you may choose to pay with life).
- does not support hybrid mana (this will be implemented soon)
- does not support generic mana costs above 9 in certain cases.

## Requirements:

Python 3.7+. pytest for running the tests.