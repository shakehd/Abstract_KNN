# -*- coding: utf-8 -*-
# =============================================================================
# File: perturbation.py
# Updated: 05/11/2022
# =============================================================================
'''Define a point perturbation'''
# =============================================================================
# Dependencies:
#   ../abstract_domains/abstract_domain.py
#   ../base.py
# =============================================================================

from abc import abstractmethod
from typing import Tuple, Type

from typings.base_types import Integer, Number, Real, String, Vector
from src.abstract_domains import AbstractDomain

class Perturbation:
    '''Represent a perturbation'''

    def __init__(self,
        feature_range: Vector[Tuple[Real, Real] | None],
        start_from: Integer = 0
    ) -> None:
        '''
        Let the class initialize the object's attributes
        :param feature_range: Minimum and maximum value of the numerical features of the points (not available = None)
        :param start_from: Feature index from which the perturbation is applied
        '''
        self.__feature_range = feature_range
        self.__start_from = start_from

    def get_feature_range(self) -> Vector[Tuple[Real, Real] | None]:
        '''
        Return minimum and maximum value of the numerical features of the points (not available = None)
        :return: Feature range
        '''
        return self.__feature_range

    def get_starting_index(self) -> Integer:
        '''
        Return the index of the feature from which the perturbation is applied
        :return: Feature from which the perturbation is applied
        '''
        return self.__start_from

    def get_type(self) -> String:
        '''
        Return the perturbation type as a string
        :return: Class name
        '''
        return self.__class__.__name__

    @abstractmethod
    def num_adv_regions(self) -> Integer:
        '''
        Return the number of adversarial regions that are (or will be) created by the perturbation
        :return: Number of adversarial regions that are (or will be) created by the perturbation
        '''
        pass

    @abstractmethod
    def perturb(self,
        point: Vector[Real],
    ) -> Vector[Type[AbstractDomain] | Number]:
        '''
        Return the adversarial region of the given point
        :param point: Point to perturb
        :return: Adversarial region of the given point
        '''
        pass