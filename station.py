from typing import NamedTuple
import numpy as np

class Station(NamedTuple):
    loc: np.ndarray

    @classmethod
    def from_string(cls, string: str):
        nums: list[int] = [int(part) for part in string.split()]  # x and y coords
        return cls(np.array(nums))
