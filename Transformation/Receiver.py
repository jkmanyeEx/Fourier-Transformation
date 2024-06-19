import matplotlib.pyplot as plt
from numpy import *
import socket

data = [[[1.0, 0.04708333333333319], [4.0, 0.45583333333333326], [8.0, 0.22875000000000045], [10.0, 0.2741666666666667]], 1.9816513761467889, 4.4]

def decode(encoded, x):
  result = 0
  for i in range(0, (encoded[0].__len__())):
    result += encoded[0][i][1] * cos(2 * pi * encoded[0][i][0] * x)

  return result * encoded[1] * encoded[2] / 2

X = [x for x in linspace(-3, 3, 1200)]
Y = [decode(data, x) for x in linspace(-3, 3, 1200)]

plt.title("Decoded Result from Receiver")
plt.plot(X, Y)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.axis([-3, 3, -3, 3])
plt.axhline(y = 0,color = 'black')
plt.axvline(x = 0, color = 'black')
plt.show()
