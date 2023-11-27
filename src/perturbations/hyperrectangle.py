# -*- coding: utf-8 -*-
# =============================================================================
# File: perturbation.py
# Updated: 05/11/2022
# =============================================================================
'''Define an hyperrectangle point parturbation'''
# =============================================================================
# Dependencies:
#   ./l_infinity.py
#   ../abstract_domains/interval.py
#   ../base.py
# =============================================================================

from typing import Tuple, Type

from .perturbation import Perturbation
from robustness import Integer, Number, Real, Vector
from robustness.abstract_domains import Interval

class Hyperrectangle(Perturbation):
    '''Represent an hyperrectangle parturbation'''
    
    def __init__(self,
        epsilons: Vector[Real],
        feature_range: Vector[Tuple[Real, Real] | None],
        start_from: Integer = 0
    ) -> None:
        '''
        Let the class initialize the object's attributes
        :param epsilons: Magnitudes of the perturbation
        :param feature_range: Minimum and maximum value of the numerical features of the points (not available = None)
        :param start_from: Feature index from which the perturbation is applied
        '''
        super().__init__(feature_range, start_from)

        self.__epsilons = epsilons
    
    def get_epsilons(self) -> Real:
        '''
        Return the magnitudes of the perturbation
        :return: Epsilon
        '''
        return self.__epsilons

    def num_adv_regions(self) -> Integer:
        '''
        Return the number of adversarial regions that are (or will be) created by the perturbation
        :return: Number of adversarial regions that are (or will be) created by the perturbation
        '''
        return 1

    def perturb(self,
        point: Vector[Real],
    ) -> Vector[Type[Interval] | Number]:
        '''
        Return the adversarial region of the given point
        :param point: Point to perturb
        :return: Adversarial region of the given point
        '''
        adv_region = point[:self.get_starting_index()]

        for feature, epsilon, range in zip(point[self.get_starting_index():], self.__epsilons, self.get_feature_range()):
            if range == None:
                adv_region.append(
                    Interval(feature - epsilon, feature + epsilon) if epsilon > 0.0 else feature
                ) 
            else:
                feature = min(max(feature, 0.0), 1.0)
                adv_region.append(
                    Interval.intersect(
                        Interval(feature - epsilon, feature + epsilon),
                        Interval(*range)
                    ) if epsilon > 0.0 else feature
                )
        
        return adv_region