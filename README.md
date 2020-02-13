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
 
 ### Coding style
 
 - PEP8
 - use python type annotations, they do wonders for completion and documentation.
 - try to describe the interface in the doc, test the interface.
 - group operations in modules, for example deck.tally takes a Deck.

## Requirements:

Python 3.7+. pytest for running the tests.