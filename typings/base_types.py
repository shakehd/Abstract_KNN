from nptyping import NDArray, Shape, Float, SignedInteger
from numpy import float_

Boolean = bool
Integer = int
Real = float
String = str
Vector = list
Set = set
Map = dict

ArrayNxM = NDArray[Shape["N, M"], Float] | NDArray[Shape["N, M"], SignedInteger]
ArrayNxN = NDArray[Shape["N, N"], Float] | NDArray[Shape["N, M"], SignedInteger]
Array1xM = NDArray[Shape["1, M"], Float] | NDArray[Shape["N, M"], SignedInteger]
NDVector  = NDArray[Shape["M"], Float] | NDArray[Shape["M"], SignedInteger] #type: ignore

Label = int

Number = Integer | Real
Literal = Number | String
