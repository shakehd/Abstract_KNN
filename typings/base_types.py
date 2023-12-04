from nptyping import NDArray, Shape, Float
from numpy import float_

ArrayNxM = NDArray[Shape["N, M"], Float]
ArrayNxN = NDArray[Shape["N, N"], Float]
Array1xM = NDArray[Shape["1, M"], Float]
NDVector  = NDArray[Shape["M"], Float]

Boolean = bool
Integer = int
Real = float | float_
String = str
Vector = list
Set = set
Map = dict

Number = Integer | Real
Literal = Number | String
