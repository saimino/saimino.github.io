---
title: "벡터의 유사도 계산 (Norm 등)방법들"
date: "2024-02-28"
tags: ["Math"]
aliases: ["tistory-31"]
source: "https://choimino.tistory.com/31"
---

## 1. 코사인 유사도 (Cosine Similarity)

코사인 유사도는 벡터간의 내적식을 이용하여, 벡터간의 유사도를 코사인 각도로 측정하는 방법이다.

$$
\mathbf{A} \cdot \mathbf{B} = \sum_{i=1}^{n} A_i B_i
$$

두 벡터가 이루는 각도의 코사인과 두 벡터 크기(제곱합의 제곱근)의 곱으로도 할 수 있으므로,

$$
\mathbf{A} \cdot \mathbf{B} = \lVert \mathbf{A} \rVert \lVert \mathbf{B} \rVert \cos(\theta)
$$

이렇게 나타 낼 수 있다. 이 식을 코사인 각도에 대하여 풀면,

$$
\text{Cosine Similarity} = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\lVert \mathbf{A} \rVert \lVert \mathbf{B} \rVert}
$$

![[31-eeaad8e5ac.jpg]]

크기가 항상 1인 단위 벡터로 표현이 가능하다. 1에 가까울수록 같은값, 0에 가까울수록 독립적인 값을 뜻한다.  
두 벡터의 유사도가 0이라면, 기저벡터로써 span할 수 있다.

여기서 코사인 각도의 크기로 얼마나 비슷한 방향을 보고 있는지로 유사도를 측정하는 것이다.  
벡터의 크기가 아닌 패턴(각도)만 보므로, 크기가 다른 벡터를 비교할 때 유용하다.

## 2. 거리 계산

### 2-1.Norm (민코프스키)

선형 대수학에서 norm은 벡터의 크기, 길이를 측정하는 방법이라고 할 수 있다. 벡터공간을 실수 값으로 mapping 해줄 수 있다는 말이다. 두 벡터의 거리를 계산하여 유사도를 측정할 수 있다.  
민코프스키 거리 라고도 한다.

$$
\lVert \mathbf{x} \rVert_p := \left( \sum_{i=1}^{n} \lvert x_i \rvert^p \right)^{1/p}
$$

p로 일반화된 norm수식 p 값에 따라 다르다. (p-norm)

![[31-1841673fe1.png]]

L1 norm과 L2 norm차이

**L1 norm (Manhattan Distance)**

$$
d = \lvert a_1 - b_1 \rvert + \lvert a_2 - b_2 \rvert
$$

p를 1로 하면 L1 norm이다.  
그림에서 볼 수 있듯이, 두 벡터의 차에 절댓값을 취해서 모두 합하면 된다.

**L2 norm (Euclidean Distance)**

$$
d = \sqrt{(a_1 - b_1)^2 + (a_2 - b_2)^2}
$$

p를 2로 하면 L2 norm이다.  
그림에서 보듯이, 그냥 피타고라스 사용한 직진거리로써, 각 원소값의 제의 제곱을 합한 후 루트를 씌운다. 가장 기본적으로 사용된다.

![[31-b549452357.png]]

L1 norm은 빨간색, 파란색, 노란색 등 많은 경로를 가지지만, L2norm은 초록색의 하나의 경로만 가진다.

**L-Infinity Norm**

p를 무한대로 놓은 것으로, 무한대로 가게되면 둘중 큰값이 남게되어 큰값을 집중하게 된다.

**Loss**

$$
\text{L1 Loss} = \sum_{i=1}^{n} \lvert y_{\text{true}} - y_{\text{predicted}} \rvert
$$

$$
\text{L2 Loss} = \sum_{i=1}^{n} \left( y_{\text{true}} - y_{\text{predicted}} \right)^2
$$

벡터의 차이를 계산하는 방법인 Norm 실제값과 예측값의 차이로 측정하여 Loss로 적용할 수도 있다.

### 2-2. Mahalanobis Distance

![[31-8d516f1057.png]]

**두 그래프에서 x, y의 거리가 같다고 할 수 있을까?** (a)에서의 xy 거리보다 (b)에서의 xy거리는 더 짧다고 해야 맞지 않을까?

이것을 수학적으로 표현하고자 하는 것이 Mahalanobis 거리이다.

$$
d(u, v) = \sqrt{(u - v) \, \Sigma^{-1} \, (u - v)^T} \qquad (\Sigma : \text{공분산 행렬})
$$

공식은 위와 같다. 식이 복잡해보이지만, 위의 Euclidean Distance에서 공분산 행렬의 역행렬 하나만 추가된 것 뿐이다.

데이터의 분포를 선형 변환 시킨후, 거리를 구하여 분포에 대해서도 고려해서 거리를 구하는 방식이다.
