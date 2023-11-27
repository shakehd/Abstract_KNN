from nptyping import NDArray, Shape, Float

ArrayNxM = NDArray[Shape["N, M"], Float]
Array1xM = NDArray[Shape["1, M"], Float]

Boolean = bool
Integer = int
Real = float
String = str
Vector = list
Set = set
Map = dict

Number = Integer | Real
Literal = Number | String