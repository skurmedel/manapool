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

print(opening_hand(deck))
