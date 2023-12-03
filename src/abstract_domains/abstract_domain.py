# -*- coding: utf-8 -*-
# =============================================================================
# File: abstract_domain.py
# Updated: 05/11/2022
# =============================================================================
'''Define an abstract domain'''
# =============================================================================
# Dependencies:
#   ../base.py
# =============================================================================

from __future__ import annotations
from abc import abstractmethod
from typing import Any, Type

from typings.base_types import Boolean, String

class AbstractDomain:
    '''Represent an abstract domain'''

    def get_type(self) -> String:
        '''
        Returns the abstract domain type as a string
        :return: Class name
        '''
        return self.__class__.__name__

    def __repr__(self) -> String:
        '''
        Represent the abstract domain as a string
        :return: The abstract domain as a string
        '''
        return self.to_string()

    @staticmethod
    @abstractmethod
    def intersect(
        abstract_domain1: Type[AbstractDomain],
        abstract_domain2: Type[AbstractDomain]
    ) -> Type[AbstractDomain] | None:
        '''
        Return the intersection of the two given abstract domains
        :param abstract_domain1: First abstract domain to intersect
        :param abstract_domain2: Second abstract domain to intersect
        :return: The intersection of the two given abstract domains
        '''
        pass

    @staticmethod
    @abstractmethod
    def join(
        abstract_domain1: Type[AbstractDomain] | None,
        abstract_domain2: Type[AbstractDomain] | None
    ) -> Type[AbstractDomain] | None:
        '''
        Return the union of the two given abstract domains
        :param interval1: First abstract domain to join
        :param interval2: Second abstract domain to join
        :return: The union of the two given abstract domains
        '''
        pass

    @abstractmethod
    def dominates(self,
        other: Type[AbstractDomain]
    ) -> Boolean:
        '''
        Return True if the abstract domain dominates the given one, otherwise return False
        :param other: Abstract domain to compare
        :return: Whether or not the abstract domain dominates the given one
        '''
        pass

    @abstractmethod
    def dominated_by(self,
        other: Type[AbstractDomain]
    ) -> Boolean:
        '''
        Return True if the abstract domain is dominated by the given one, otherwise return False
        :param other: Abstract domain to compare
        :return: Whether or not the abstract domain is dominated by the given one
        '''
        pass

    @abstractmethod
    def strictly_dominates(self,
        other: Type[AbstractDomain]
    ) -> Boolean:
        '''
        Return True if the abstract domain strictly dominates the given one, otherwise return False
        :param other: Abstract domain to compare
        :return: Whether or not the abstract domain strictly dominates the given one
        '''
        pass

    @abstractmethod
    def strictly_dominated_by(self,
        other: Type[AbstractDomain]
    ) -> Boolean:
        '''
        Return True if the abstract domain is strictly dominated by the given one, otherwise return False
        :param other: Abstract domain to compare
        :return: Whether or not the abstract domain is strictly dominated by the given one
        '''
        pass

    @abstractmethod
    def to_string(self) -> String:
        '''
        Return the abstract domain information as a string
        :return: The abstract domain as a string
        '''
        pass

    @abstractmethod
    def to_python_type(self) -> Any:
        '''
        Return the abstract domain information using the best python type to represent them
        :return: The abstract domain as python type
        '''
        pass