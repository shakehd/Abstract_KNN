from dataclasses import dataclass
from typing import List, Self
from typings.base_types import Array1xM, Real, String
import numpy as np

@dataclass(init=False)
class Hyperplane:

    def __init__(self: Self, coefficients: Array1xM | None = None,
                 constant: np.float_ = np.float_(), dimensions: int =0):
        if coefficients is None:
            coefficients = np.zeros(dimensions)

        self.coefficients: Array1xM = coefficients
        self.constant: np.float_ = constant

    def  distance_to_point(self: Self, p:Array1xM)-> np.float_:
        coefs_norm: np.float_ = np.linalg.norm(self.coefficients)
        return abs((np.dot(self.coefficients, p) - self.constant)) / coefs_norm


    def __call__(self: Self, p:Array1xM) -> Real:
        return np.dot(self.coefficients, p) + self.constant


    def __str__(self: Self) -> String:
        coefs_repr: List[str] = [f"{self.coefficients[i]} x_{i}"
                                 for i in range(0, self.coefficients.shape[0])]
        return ' + '.join(coefs_repr) + f" + {self.constant} = 0"