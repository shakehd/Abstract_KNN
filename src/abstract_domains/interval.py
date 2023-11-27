from __future__ import annotations
from dataclasses import dataclass
from typing import Self

from typings.base_types import Vector, Boolean, Integer, Number, String

from .abstract_domain import AbstractDomain


@dataclass
class Interval(AbstractDomain['Interval']):
    '''Represent the interval abstract domain'''

    lb: Number
    ub: Number

    @staticmethod
    def intersect(
        domain1: Interval | None,
        domain2: Interval | None
    ) -> Interval | None:
        '''
        Return the intersection of the two given intervals
        :param interval1: First interval to intersect
        :param interval2: Second interval to intersect
        :return: The intersection of the two given intervals
        '''
        if domain1 is None or domain2 is None:
            return None

        lb = max(domain1.lb, domain2.lb)
        ub = min(domain1.ub, domain2.ub)

        return Interval(lb, ub) if lb <= ub else None

    @staticmethod
    def join(
        domain1: Interval | None,
        domain2: Interval | None
    ) -> Interval | None:
        '''
        Return the union of the two given intervals
        :param interval1: First interval to join
        :param interval2: Second interval to join
        :return: The union of the two given intervals
        '''
        if domain1 == None:
            return domain2
        if domain2 == None:
            return domain1

        return Interval(min(domain1.lb, domain2.lb), max(domain1.ub, domain2.ub))

    def dominates(self: Self,
        other: Interval | Number
    ) -> Boolean:
        '''
        Return True if the interval dominates the given one, otherwise return False
        :param other: Interval to compare
        :return: Whether or not the interval dominates the given one
        '''
        if issubclass(type(other), Interval):
            return self.lb >= other.ub #type: ignore
        return self.lb >= other #type: ignore

    def dominated_by(self: Self,
        other: Interval | Number
    ) -> Boolean:
        '''
        Return True if the interval is dominated by the given one, otherwise return False
        :param other: Interval to compare
        :return: Whether or not the interval is dominated by the given one
        '''

        if isinstance(other, Interval):
            return self.ub <= other.lb

        return self.ub <= other

    def strictly_dominates(self: Self,
        other: Interval | Number
    ) -> Boolean:
        '''
        Return True if the interval strictly dominates the given one, otherwise return False
        :param other: Interval to compare
        :return: Whether or not the interval strictly dominates the given one
        '''
        if isinstance(other, Interval):
            return self.lb > other.ub
        return self.lb > other

    def strictly_dominated_by(self: Self,
        other: Interval | Number
    ) -> Boolean:
        '''
        Return True if the interval is strictly dominated by the given one, otherwise return False
        :param other: Interval to compare
        :return: Whether or not the interval is strictly dominated by the given one
        '''
        if isinstance(other, Interval):
            return self.ub < other.lb
        return self.ub < other

    def to_string(self) -> String:
        '''
        Return the interval as a string
        :return: The interval as a string
        '''
        return '[{}, {}]'.format(self.lb, self.ub)

    def to_python_type(self) -> Vector[Number]:
        '''
        Return the interval as a vector [lb, ub]
        :return: The interval as a vector
        '''
        return [self.lb, self.ub]

    def __lt__(self: Self,
        other: Interval | Number
    ) -> Boolean:
        '''
        Overloading of the less then comparison operator
        :param other: Interval to compare
        :return: Whether or not the interval has a lower bound less than that of the given one
        '''
        # Note: it does not coincide with the partial order of the domain’s lattice
        if isinstance(other, Interval):
            return self.lb < other.lb or (self.lb == other.lb and self.ub < other.ub)
        return self.lb < other

    def __add__(self: Self,
        other: Interval | Number
    ) -> Interval:
        '''
        Overloading of the addition operator
        :param other: Second addend
        :return: Result of the sum
        '''
        if isinstance(other, Interval):
            return Interval(self.lb + other.lb, self.ub + other.ub)
        return Interval(self.lb + other, self.ub + other)

    def __sub__(self: Self,
        other: Interval | Number
    ) -> Interval:
        '''
        Overloading of the subtraction operator
        :param other: Subtrahend
        :return: Result of the difference
        '''
        if isinstance(other, Interval):
            return Interval(self.lb - other.ub, self.ub - other.lb)
        return Interval(self.lb - other, self.ub - other)

    def __mul__(self: Self,
        other: Interval | Number
    ) -> Interval:
        '''
        Overloading of the multiplication operator
        :param other: Second factor
        :return: Result of multiplication
        '''
        if isinstance(other, Interval):
            return Interval(
                min(self.lb * other.lb, self.lb * other.ub, self.ub * other.lb, self.ub * other.ub),
                max(self.lb * other.lb, self.lb * other.ub, self.ub * other.lb, self.ub * other.ub)
            )
        return Interval(
            min(self.lb * other, self.lb * other, self.ub * other, self.ub * other),
            max(self.lb * other, self.lb * other, self.ub * other, self.ub * other)
        )


    def __abs__(self: Self) -> Interval:
        '''
        Overloading of the absolute value operator
        :return: Absolute value of the object
        '''
        if self.lb * self.ub >= 0:
            return Interval(min(abs(self.lb), abs(self.ub)), max(abs(self.lb), abs(self.ub)))
        return Interval(0, max(abs(self.lb), abs(self.ub)))

    def __pow__(self: Self,
        n: Integer
    ) -> Interval:
        '''
        Overloading of the exponentiation operator
        :param n: Exponent
        :return: Result of the exponentiation
        '''
        if self.lb >= 0 or (n % 2) != 0:
            return Interval(self.lb ** n, self.ub ** n)
        if self.ub < 0:
            return Interval(self.ub ** n, self.lb ** n)
        return Interval(0, max(self.lb ** n, self.ub ** n))