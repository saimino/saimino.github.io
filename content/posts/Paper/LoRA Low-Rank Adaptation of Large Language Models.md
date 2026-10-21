---
title: "LoRA: Low-Rank Adaptation of Large Language Models"
date: "2024-08-10"
tags: ["Paper"]
aliases: ["tistory-36"]
source: "https://choimino.tistory.com/36"
---

**paper:<https://arxiv.org/abs/2106.09685>**

[LoRA: Low-Rank Adaptation of Large Language Models

An important paradigm of natural language processing consists of large-scale pre-training on general domain data and adaptation to particular tasks or domains. As we pre-train larger models, full fine-tuning, which retrains all model parameters, becomes le

arxiv.org](https://arxiv.org/abs/2106.09685)

**code:<https://github.com/microsoft/LoRA>**

[GitHub - microsoft/LoRA: Code for loralib, an implementation of "LoRA: Low-Rank Adaptation of Large Language Models"

Code for loralib, an implementation of "LoRA: Low-Rank Adaptation of Large Language Models" - microsoft/LoRA

github.com](https://github.com/microsoft/LoRA)

### 1. Introduction

LoRA가 등장한 배경은, 프리트레인된 모델을 파인튜닝할 때 발생하는 **메모리 문제**에 있다.

GPT처럼 175B 파라미터를 가진 모델은 단순히 올리는 것만으로도 막대한 메모리가 필요하다. 여기에 그라디언트 계산용 텐서, 옵티마이저의 모멘텀 기록 등 추가 메모리 소모가 발생한다.

모델 규모는 커지고 있지만 하드웨어는 제한적이기 때문에, 파라미터 업데이트를 효율화하는 다양한 방법이 등장했다. LoRA 역시 그 중 하나다.

저자들은 "모델은 거대하지만 실제로는 고유 차원(intrinsic dimensionality)이 낮다"는 기존 연구들에서 모티브를 얻었다.

참고 논문:  
[**Intrinsic Dimensionality Explains the Effectiveness of Language Model Fine-Tuning**](https://arxiv.org/abs/2012.13255)  
[**Measuring the Intrinsic Dimension of Objective Landscapes**](https://arxiv.org/abs/1804.08838)

LoRA는 "실제로 업데이트가 필요한 가중치는 적다"는 가설을 세우고 시작한다.

기존 풀파인튜닝은 모든 파라미터를 업데이트하는 방식을 따른다.

![[36-733fffa977.png]]

fully fine tune

반면 LoRA는 전체 파라미터를 건드리지 않고, 일부 저차원 공간만 업데이트하는 방식을 택한다.

![[36-0747201481.png]]

LoRA

---

### 2. AREN'T EXISTING SOLUTIONS GOOD ENOUGH?

LoRA가 등장하기 전에도 파라미터 이피션트 튜닝 기법은 존재했다. 대표적인 것이 **Adapter**다.

![[36-bdaf778bf8.png]]

Adapter (그림은 QLoRA에서 따옴)

Adapter는 전체 모델을 프리즈하고, 다운 프로젝션과 업 프로젝션 두 개의 작은 행렬만 학습한다.

하지만 이 방식은 **Sequential 연산**을 강제하기 때문에 **추론 지연(latency)** 문제가 생긴다. 특히 멀티 헤드 어텐션 결과를 받아야 연산이 진행되기 때문에 속도 저하가 발생한다.

LoRA 논문 3장에서도, 기존 Adapter 방식은 충분히 빠르지 않고 효율적이지 못하다고 지적한다.

---

### 4. OUR METHOD

LoRA는 Adapter와 구조는 유사하지만, 훨씬 빠르고 효율적인 방법을 제시한다.

![[36-5ee324e145.png]]

![[36-3bf20def6c.png]]

LoRA는 다운 프로젝션(A)과 업 프로젝션(B) 두 개의 작은 행렬을 사용해 가중치 업데이트를 근사한다.

기존 모델 가중치는 프리즈시키고, BA 행렬만 학습한다. 입력 x는 원래 pretrained weight(W₀)과 BA 업데이트를 각각 통과한 후 합산된다.

![[36-234439903a.png]]

github code (LoRA)

LoRA 공식 GitHub 코드에서는 PyTorch의 Linear 클래스를 상속해 A, B 매트릭스를 별도로 정의한다.

**LoRA의 장점 요약:**

- BA 매트릭스를 기존 가중치에 합칠 수 있어, 별도의 Adapter 레이어 없이 바로 사용 가능하다.
- 추론 시 latency가 발생하지 않는다.
- 다른 downstream task로 쉽게 전환할 수 있다. (BA만 교체)

### 999. Result

![[36-f14ee39754.png]]

논문참조
