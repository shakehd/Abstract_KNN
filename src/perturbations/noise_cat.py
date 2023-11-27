# -*- coding: utf-8 -*-
# =============================================================================
# File: noise_cat.py
# Updated: 05/11/2022
# =============================================================================
'''Define a NOISE-CAT parturbation'''
# =============================================================================
# Dependencies:
#   ./perturbation.py
#   ../abstract_domains/interval.py
#   ../base.py
# =============================================================================

from itertools import product
from typing import Tuple, Type

from .perturbation import Perturbation
from typings.base_types import Integer, Number, Real, Vector
from src.abstract_domains import Interval

class NoiseCat(Perturbation):
    '''Represent a NOISE-CAT parturbation'''

    def __init__(self,
        noise: Type[Perturbation],
        cat_indexes: Vector[Tuple[Integer, Integer]],
    ) -> None:
        '''
        Let the class initialize the object's attributes
        :param noise:
        :param cat_indexes: Indexes of the features involved in the CAT perturbation in the form [(from_index, num_values)]
        '''
        self.__noise = noise
        self.__cat_indexes = cat_indexes
        self.__point = None
        self.__num_adv_regions = 1

        self.__possible_values = {}
        for _, num_values in cat_indexes:
            if not num_values in self.__possible_values:
                if num_values == 1:
                    self.__possible_values[num_values] = [[0.0]]
                elif num_values == 2:
                    self.__possible_values[num_values] = [[1.0], [0.0]]
                else:
                    self.__possible_values[num_values] = [[0.0 for _ in range(num_values)] for _ in range(num_values)]
                    for i, features  in enumerate(self.__possible_values[num_values]):
                        features[i] = 1.0
            self.__num_adv_regions *= num_values

    def get_noise(self) -> Type[Perturbation]:
        '''
        Return the noise that is (or wiil be) applied to a point
        :return: Noise that is (or wiil be) applied to a point
        '''
        return self.__noise

    def get_cat_indexes(self) -> Integer:
        '''
        Return the indexs of the features involved in the CAT perturbation in the form [(from_index, num_values)]
        :return: Indexes of the features involved in the CAT perturbation
        '''
        return self.__cat_indexes

    def num_adv_regions(self) -> Integer:
        '''
        Return the number of adversarial regions that are (or will be) created by the perturbation
        :return: Number of adversarial regions that are (or will be) created by the perturbation
        '''
        return self.__num_adv_regions

    def perturb(self,
        point: Vector[Real],
    ) -> Vector[Type[Interval] | Number] | None:
        '''
        Return the adversarial region of the given point
        :param point: Point to perturb
        :return: Adversarial region of the given point
        '''
        if self.__point != point:
            self.__point = point
            self.__adv_region = self.__noise.perturb(point)
            self.__cartesian_product = product(
                *[self.__possible_values[num_values] for _, num_values in self.__cat_indexes]
            )
        try:
            next_combination = next(self.__cartesian_product)
        except StopIteration:
            # all possible combinations of 0,1 forming a valid one-hot sequence (or sequences)
            self.__cartesian_product = product(
                *[self.__possible_values[num_values] for _, num_values in self.__cat_indexes]
            )
            next_combination = next(self.__cartesian_product)

        for (from_index, _), features in zip(self.__cat_indexes, next_combination):
            for i, feature in enumerate(features):
                self.__adv_region[from_index + i] = feature

        return self.__adv_region