import matplotlib.pyplot as plt
from numpy import *
import socket

data = []

def decode(encoded, x):
  result = 0
  for i in range(0, (encoded[0].__len__())):
    result += encoded[0][i][1] * cos(2 * pi * encoded[0][i][0] * x)

  return result * encoded[1] * encoded[2] / 2

X = [x for x in linspace(-3, 3, 1200)]
Y = [decode(eval(data), x) for x in linspace(-3, 3, 1200)]

plt.title("Decoded Result from Receiver")
plt.plot(X, Y)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.axis([-3, 3, -3, 3])
plt.axhline(y = 0,color = 'black')
plt.axvline(x = 0, color = 'black')
plt.show()
