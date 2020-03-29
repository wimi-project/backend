import logging
from functools import reduce
from typing import List

logger = logging.getLogger("main")


def square_exponents(num: int = 20) -> List[int]:
    exponents = []
    for i in range(num):
        exponents.append(2**i)
    return exponents


def compute_square_exponential_mean(values: List[int]) -> float:
    exponents = square_exponents(len(values))
    num = 0
    idx = 0
    for value in values:
        num += value * exponents[idx]
        idx += 1
    den = reduce((lambda x, y: x + y), exponents)
    return num / den
