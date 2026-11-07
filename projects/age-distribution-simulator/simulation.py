"""Generate synthetic ages with a local, reproducible random generator."""
import random

def simulate(size=8000, minimum=13, maximum=80, seed=123):
    for value in (size, minimum, maximum, seed):
        if type(value) is not int:
            raise ValueError('Size, bounds and seed must be integers')
    if size < 1 or not 0 <= minimum <= maximum <= 120:
        raise ValueError('Use positive size and 0 <= minimum <= maximum <= 120')
    rng = random.Random(seed)
    return [rng.randint(minimum, maximum) for _ in range(size)]
