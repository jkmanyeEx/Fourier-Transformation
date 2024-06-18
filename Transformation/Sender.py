import matplotlib.pyplot as plt
from numpy import *
import socket

fWave = [1, 4, 8, 10]
strengthWave = [0.2, 2, 1, 1.2]

def original(x):
  result = 0
  for f in [0, 1, 2, 3]:
    result += cos(2 * pi * fWave[f] * x) * strengthWave[f]
  return result

X = [x for x in linspace(-3, 3, 1200)]
Y = [original(x) for x in linspace(-3, 3, 1200)]

plt.title("Original Graph")
plt.plot(X, Y)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.axis([-3, 3, -3, 3])
plt.axhline(y = 0,color = 'black')
plt.axvline(x = 0, color = 'black')
plt.show()

def maxval():
  maxVal = 0
  for x in linspace(-3, 3, 1200):
    maxVal = max(maxVal, original(x))

  return maxVal

maxValue = maxval()

def wave(x):
  return original(x) / maxValue * 2

print("Multiplier for original wave: " + str(maxval()))

X = [x for x in linspace(-3, 3, 1200)]
Y = [wave(x) for x in linspace(-3, 3, 1200)]

plt.title("Original Graph Calculated With Calibrated Multiplier")
plt.plot(X, Y)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.axis([-3, 3, -3, 3])
plt.axhline(y = 0,color = 'black')
plt.axvline(x = 0, color = 'black')
plt.show()

fWind = int(input("Type in the Winding Frequency You Want: "))

def wind(x, f):
  return wave(x) * exp(-1j * x * 2 * pi * f)

Z = [wind(x, fWind) for x in linspace(0, 6, 1200)]

plt.title("Winded Graph (Freq: " + str(fWind) + ")")
plt.plot(real(Z), imag(Z))
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.axis([-3, 3, -3, 3])
plt.axhline(y = 0,color = 'black')
plt.axvline(x = 0, color = 'black')

N = 0

for x in linspace(0, 6, 1200):
  N += wind(x, fWind)

plt.plot(real(N / 1200), 0, 'ro')
# print(real(N / 1200))

plt.show()

def gravityCenter(f):
  N = 0
  for x in linspace(0, 6, 1200):
    N += wind(x, f)
  return real(N / 1200)

# for f in linspace(1, 100, 1189):
#   plt.plot(f, gravityCenter(f), 'ro')

# plt.xlabel('Freq')
# plt.ylabel('Center')
# plt.axis([0, 10, -1, 1])
# plt.axhline(y = 0,color = 'black')
# plt.axvline(x = 0, color = 'black')

# plt.show()

resultArray = [[0, 0]]

for f in linspace(1, 100, 1189):
  centerVal = gravityCenter(f)
  if (centerVal >= 0.03):
    if (abs(f - resultArray[-1][0]) >= 1):
      resultArray.append([f, centerVal])
      plt.plot(f, centerVal, 'ro')
    else:
      if (resultArray[-1][1] < centerVal):
        resultArray.pop()
        resultArray.append([f, centerVal])
        plt.plot(f, centerVal, 'ro')

resultArray.pop(0)

print("Frequency and Strength of Original Wave: " + str(resultArray))

plt.title("Center of the Mass Depending on the Freqency (Filtered)")
plt.xlabel('Freq')
plt.ylabel('Center')
plt.axis([0, 10, -1, 1])
plt.axhline(y = 0,color = 'black')
plt.axvline(x = 0, color = 'black')
plt.axhline(y = 0.03,color = 'blue')

plt.show()

def inverse(x):
  result = 0
  for i in range(0, (resultArray.__len__())):
    result += resultArray[i][1] * cos(2 * pi * resultArray[i][0] * x)

  return result

X = [x for x in linspace(-3, 3, 1200)]
Y = [inverse(x) for x in linspace(-3, 3, 1200)]

plt.title("Inversed Graph from [resultArray]")
plt.plot(X, Y)
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.axis([-3, 3, -3, 3])
plt.axhline(y = 0,color = 'black')
plt.axvline(x = 0, color = 'black')
plt.show()

def multiplier():
  n = 0
  for k in linspace(0, 6, 1200):
    if ((wave(0) - (inverse(0) * k)) <= 0.01):
        n = k
        break
        
  return n

def result():
  return [resultArray, multiplier(), maxValue]

print("Final Exported Result: " + str(result()))
