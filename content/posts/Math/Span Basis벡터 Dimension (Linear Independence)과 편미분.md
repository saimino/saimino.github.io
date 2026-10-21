---
title: "Span Basis벡터 Dimension (Linear Independence)과 편미분"
date: "2024-02-25"
tags: ["Math"]
aliases: ["tistory-29"]
source: "https://choimino.tistory.com/29"
---

#### 1. Span, Basis, Dimension, Linear Independence

**Span**은 주어진 벡터 집합을 스칼라 배로 조합하여 만들 수 있는 모든 벡터의 집합을 의미한다.

**Basis**는 한 벡터 공간 전체를 생성할 수 있는 선형 독립인 벡터들의 집합을 의미한다. 즉, Basis는 공간을 중복 없이 최소한의 수로 생성하는 벡터들의 집합이다.

**Dimension**은 Basis를 구성하는 벡터의 수를 의미한다. 예를 들어, 3차원 공간의 경우 Basis는 3개의 선형 독립인 벡터로 구성되며, 이때 Dimension은 3이다.

**Linear Independence**란 벡터 집합 내 어떤 벡터도 나머지 벡터들의 선형 결합으로 표현될 수 없다는 성질을 의미한다. 선형 독립인 벡터들만으로 Basis를 정의할 수 있다.

정리하면, 선형 독립인 벡터들의 집합(Basis)을 통해 Span을 형성하며, 그 벡터들의 수가 해당 공간의 Dimension을 결정한다.

---

#### 2. 편미분

편미분은 다변수 함수에서 하나의 변수를 선택하여 그 변수에 대해서만 미분을 수행하고, 나머지 변수들은 상수로 취급하는 연산이다.

![[29-a235d0868e.png]]

z를 x에 대해 편미분

예제:

![[29-93e41489be.png]]

위 식에서 x에 대해 편미분을 수행할 때, y에 대한 항들은 상수로 간주하여 편미분 결과에 영향을 주지 않는다. 결과적으로 y² 항은 편미분 시 0이 된다.

편미분은 딥러닝 모델에서 역전파(Backpropagation)를 구현할 때 필수적으로 사용된다.

---

#### 3. Chain Rule과 Backpropagation

딥러닝에서 파라미터 업데이트를 위해 오류를 역전파할 때, 편미분과 연쇄법칙(chain rule)이 결합되어 사용된다.

![[29-bede505a6e.png]]

chain rule

Chain Rule을 이용하면, 복합 함수의 미분을 각 함수별 편미분의 곱으로 표현할 수 있다. 예를 들어, z가 y에, y가 x에 종속될 때, z를 x에 대해 미분하는 것은 다음과 같이 표현된다.

\[ \frac{\partial z}{\partial x} = \frac{\partial z}{\partial y} \times \frac{\partial y}{\partial x} \]

이러한 수식 구조를 통해 딥러닝에서는 출력층부터 입력층까지 오류를 효율적으로 전파하며 학습을 수행한다.
