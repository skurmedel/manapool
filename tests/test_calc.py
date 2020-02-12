from manapool import calc


def test_binomial():
    assert (calc.binomial(5, 0) == 1)
    assert (calc.binomial(5, 4) == calc.binomial(5, 1))
    assert (calc.binomial(5, 1) == 5)

    assert (calc.binomial(5, 3) == 10)
