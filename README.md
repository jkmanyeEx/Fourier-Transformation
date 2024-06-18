# 이산 푸리에 변환의 구현 (2023.12)

## 개요

본 탐구에서는 python의 numpy와 matplotlib을 이용하여 이산 푸리에 변환 (DFT)의 알고리즘을 구현하였다.

## 이론

### 푸리에 변환과 이산 푸리에 변환

푸리에 변환(Fourier transform, FT)은 시간이나 공간에 대한 함수를 시간 또는 공간 주파수 성분으로 분해하는 변환을 말한다. 푸리에 변환은 이 변환으로 나타난 주파수 영역에서 함수를 표현한 결과물을 가리키는 용어로도 종종 사용된다.

이산 푸리에 변환(Discrete Fourier Transform, DFT)은 이산적인 입력 신호에 대한 푸리에 변환으로, 디지털 신호 분석과 같은 분야에 사용된다. 이산 푸리에 변환은 고속 푸리에 변환(Fast Fourier Transform,FFT)을 이용해 빠르게 계산할 수 있지만, 이 탐구에서는 고전적인 DFT의 방법만 구현한다.

푸리에 변환은 무한한 시간 연속적 신호를 적분하는 반면, 이산 푸리에 변환은 측정된 샘플을 모두 더하여 샘플의 수로 나누는 방법을 채택한다.

식으로는 다음과 같이 나타난다.

![img](https://wikimedia.org/api/rest_v1/media/math/render/svg/334fa0b082627eb35bf5bde5501cc95b6a1656a1)

푸리에 변환의 원리는, 특정 주파수를 성분으로 갖는 파동을 그 주파수만큼 그래프를 감았을 때에 특정 형태가 나온다는 점을 이용한다. 이를 복소평면상에서 허수를 정의역으로 갖는 지수함수를 이용하여 회전을 표현하고, 그에 함숫값을 곱한다면 감은 그래프가 된다. 따라서 이 그래프 위의 유한한 점들을 잡고 그 점들의 좌푯값들의 평균을 내어 이 주파수가 주어진 함수의 성분인지 아닌지를 판단하는 것이다.

## 구현

### 1. 파동 생성

임의의 주파수와 그에 해당하는 세기를 가진 리스트를 생성 후 그를 바탕으로 파동을 만든다.
```python
fWave = [1, 4, 8, 10]
strengthWave = [0.2, 2, 1, 1.2]

def original(x):
  result = 0
  for f in [0, 1, 2, 3]:
    result += cos(2 * pi * fWave[f] * x) * strengthWave[f]
  return result

X = [x for x in linspace(-3, 3, 1200)]
Y = [original(x) for x in linspace(-3, 3, 1200)]
```
그리고, 이 함수의 진폭을 일정하게 조정하여 변환하기 쉽도록 한다.
```python
def maxval():
  maxVal = 0
  for x in linspace(-3, 3, 1200):
    maxVal = max(maxVal, original(x))

  return maxVal

maxValue = maxval()

def wave(x):
  return original(x) / maxValue * 2
```
이제, 복소평면 상에서 함수의 그래프를 '감는다'는 것을 표현한다.
```python
fWind = int(input("Type in the Winding Frequency You Want: "))

def wind(x, f):
  return wave(x) * exp(-1j * x * 2 * pi * f)

Z = [wind(x, fWind) for x in linspace(0, 6, 1200)]
# Z는 주파수 성분 fWind에 대한 감긴 복소수 함숫값
```
이를 주파수 1189개에 대하여 반복하고, 특정 세기 이상의 주파수들만 저장한다.
```python
def gravityCenter(f):
  N = 0
  for x in linspace(0, 6, 1200):
    N += wind(x, f)
  return real(N / 1200)

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
```
마지막으로, 결과 리스트를 이용해 파동을 그리고, 이 파동을 원래 함수의 진폭에 맞게 고쳐 내보낸다.
```python
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
```
이제, 원래의 파동을 모르는 상태에서 위의 출력값만을 가지고 원래 파동을 나타낼 수 있다.
```python
def decode(encoded, x):
  result = 0
  for i in range(0, (encoded[0].__len__())):
    result += encoded[0][i][1] * cos(2 * pi * encoded[0][i][0] * x)

  return result * encoded[1] * encoded[2] / 2
```

## 해석 & 결론

본 탐구에서 푸리에 변환이 무엇인지와, 이를 실생활애서 어디에 사용하는지, 그리고 이 변환의 수학적 원리를 깨달을 수 있었다. 다음에는 이를 고속 푸리에 변환으로 구현하고, 소켓 통신을 추가하여 실제 통화 기능도 구현하고 싶다.

## 소스 코드 링크

https://github.com/jkmanyeEx/Fourier-Transformation