import itertools

COINS_BY_LABEL = {
    'red': 2,
    'blue': 9,
    'shiny': 5,
    'corroded': 3,
    'concave': 7
}
COINS_BY_VALUE = dict(zip(COINS_BY_LABEL.values(), COINS_BY_LABEL.keys()))

for values in itertools.permutations(COINS_BY_VALUE.keys()):
  a, b, c, d, e = values
  if a + b * c**2 + d**3 - e == 399:
    labels = [COINS_BY_VALUE[v] for v in values]
    print('{} + {} * {}**2 + {}**3 - {}'.format(*values))
    print('{} + {} * {}**2 + {}**3 - {}'.format(*labels))
    break
