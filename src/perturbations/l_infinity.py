# -*- coding: utf-8 -*-
# =============================================================================
# File: norm_infinity.py
# Updated: 05/11/2022
# =============================================================================
'''Define a L-infinity point parturbation'''
# =============================================================================
# Dependencies:
#   ./perturbation.py
#   ../abstract_domains/interval.py
#   ../base.py
# =============================================================================

from typing import Tuple, Type

from .perturbation import Perturbation
from robustness import Integer, Number, Real, Vector
from robustness.abstract_domains import Interval

class Linfinity(Perturbation):
    '''Represent a L-infinity parturbation'''
    
    def __init__(self,
        epsilon: Real,
        feature_range: Vector[Tuple[Real, Real] | None],
        start_from: Integer = 0
    ) -> None:
        '''
        Let the class initialize the object's attributes
        :param epsilon: Magnitude of the perturbation
        :param feature_range: Minimum and maximum value of the numerical features of the points (not available = None)
        :param start_from: Feature index from which the perturbation is applied
        '''
        super().__init__(feature_range, start_from)

        self.__epsilon = epsilon
    
    def get_epsilon(self) -> Real:
        '''
        Return the magnitude of the perturbation
        :return: Epsilon
        '''
        return self.__epsilon
    
    def num_adv_regions(self) -> Integer:
        '''
        Return the number of adversarial regions that are (or will be) created by the perturbation
        :return: Number of adversarial regions that are (or will be) created by the perturbation
        '''
        return 1

    def perturb(self,
        point: Vector[Real],
    ) -> Vector[Type[Interval]] | Vector[Number]:
        '''
        Return the adversarial region of the given point
        :param point: Point to perturb
        :return: Adversarial region of the given point
        '''
        adv_region = point[:self.get_starting_index()]

        if self.__epsilon == 0.0:
            for feature, range in zip(point[self.get_starting_index():], self.get_feature_range()):
                adv_region.append(feature if range == None else min(max(feature, 0.0), 1.0))    
        else:
            for feature, range in zip(point[self.get_starting_index():], self.get_feature_range()):
                if range == None:
                    adv_region.append(
                        Interval(feature - self.__epsilon, feature + self.__epsilon)
                    ) 
                else:
                    feature = min(max(feature, 0.0), 1.0)
                    adv_region.append(
                        Interval.intersect(
                            Interval(feature - self.__epsilon, feature + self.__epsilon),
                            Interval(*range)
                        )
                    )
        
        return adv_region