from nptyping import NDArray, Shape, Float, SignedInteger
from numpy import float_

Boolean = bool
Integer = int
Real = float
String = str
Vector = list
Set = set
Map = dict

ArrayNxM = NDArray[Shape["N, M"], Float | SignedInteger]
ArrayNxN = NDArray[Shape["N, N"], Float | SignedInteger]
Array1xM = NDArray[Shape["1, M"], Float | SignedInteger ]
NDVector  = NDArray[Shape["M, "], Float | SignedInteger]


Number = Integer | Real
Literal = Number | String
