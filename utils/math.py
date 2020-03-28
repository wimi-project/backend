from typing import List
from functools import reduce


def square_exponents(num: int = 20) -> List[int]:
    exponents = []
    for i in range(num):
        exponents.append(2**i)
    return exponents


def compute_square_exponential_mean(values: List[int]) -> float:
    exponents = square_exponents(len(values))
    num = 0
    idx = 0
    for value in range(len(values)):
        num += value * exponents[idx]
    den = reduce((lambda x, y: x + y), exponents)
    return num / den
