---
title: "GPT Understands, Too"
date: "2024-08-12"
tags: ["Paper"]
aliases: ["tistory-38"]
source: "https://choimino.tistory.com/38"
---

## 개요

이 논문은 프롬프트에 학습가능한 임베딩 벡터를 추가해서 파인튜닝하는 방법인 **P-Tuning**을 처음 소개하였다.  
AI Open Journal 2023에 출판되었다.

사전 학습된 언어 모델(PLMs)은 자연어 이해(NLU) 분야의 성능을 향상시켰다.  
PLMs는 마스크드 언어 모델링, 오토리그레시브 언어 모델링, 시퀀스 투 시퀀스 모델링 등을 통해 훈련되었다.

프롬프트를 활용하면 PLM을 소규모 라벨링 데이터로 파인튜닝하거나, 모델을 프리즈한 상태로 다운스트림 태스크에 사용할 수 있다.  
프롬프트 기반 학습은 여러 NLU 태스크에서 성능을 개선하는 데 사용되었다.

---

## 문제

![[38-94b7ba4173.png]]

수작업으로 작성된 discrete prompt는 불안정성을 가진다.

- 프롬프트에서 단어 하나만 변경해도 성능이 하락할 수 있다.
- 예시: "이 도시는 어디에 있나요?" → "이 도시는 어느 나라에 있나요?" 로 변경했을 때 성능 저하 발생

few-shot 세팅에서는 이러한 문제가 더 두드러진다고 한다.  
discrete prompt 불안정성때문에 적용이 잘 안된다고 한다.

기존 연구들은 **자동으로 프롬프트를 탐색하는 방법을** 시도하였다.

- 학습 데이터 코퍼스를 기반으로 검색
- 그래디언트 기반 탐색
- 생성 모델을 통한 프롬프트 생성

이 접근법들은 discrete prompt 자체의 딱딱 나눠져서 생기는 불안정성을 해결하지 못했다.  
또한, 이렇게 분리된 공간적 정보에서는 역전파를 효과적으로 활용할 수 없다고 한다.

---

## P-Tuning

**P-Tuning**은 디스크리트 프롬프트의 불안정성을 완화하기 위해 제안되었다.

핵심 내용은 다음과 같다.

- 입력 프롬프트에 **continuous 프롬프트 임베딩** 추가
- **continuous**임베딩을 backpropagation을 통해 학습
- 자연어 프롬프트의 작은 변화에 의한 성능 저하를 완화

모델 설정:

- `M`: 프리트레인된 언어 모델 (hidden size = h, vocabulary size = |V|)
- `{(xi, yi)}`: NLU 태스크에 대한 라벨링된 데이터셋
- 목표: 조건부 확률 ( p(y|x) ) 추정

기존 프롬프트 방식:

> "The capital of [INPUT] is [LABEL]."

예시:

> (Britain, London) → "The capital of Britain is [MASK]."

디스크리트 프롬프트와 입력 데이터를 함께 인베딩하여 모델에 입력한다.

---

## 구조

![[38-4dc44e1859.png]]

P-Tuning은 연속형 임베딩을 사용한다.

- 각 continuous prompt embedding `Pi`를 학습
- 임베딩 함수 ( f(P_i) )를 통해 입력 공간에 매핑
- 최종 입력 시퀀스:

[  
{h_0, h_1, ..., h_i, e(x), h_{i+1}, ..., h_j, e(y), h_{j+1}, ..., h_k}  
]

descrete 프롬프트와 continuous 프롬프트를 조합할 수 있고, 성능이 더 높다.  
P-Tuning은 모델이 frezen되었거나 파인튜닝된 상태 모두에 적용 가능하다.

---

## Prompt Encoder

프롬프트 간 의존성을 모델링하기 위해  
<strong>프롬프트 인코더(prompt encoder)</strong>를 사용한다.

- 임베딩 함수 `f`를 통해 연속형 프롬프트 간 관계를 학습
- 구현 방법: LSTM, MLP, 또는 Identity 함수

---

## 실험

P-Tuning은 두 가지 벤치마크에서 실험되었다.

- **LAMA** (knowledge probing)
- **SuperGLUE** (NLU benchmark)
- LAMA 태스크에서는, 언어 모델을 프리즈한 상태에서도 수작업 프롬프트 대비 20포인트 이상, 검색 기반 프롬프트 대비 9포인트 성능 향상
- SuperGLUE 태스크에서는 기존 방식(PET)보다 높은 성능을 기록

또한, 프롬프트 간 성능 편차를 줄여 언어 모델 적응의 안정성을 높였다고 한다.  
  
(자세한 실험내용은 논문 참조.)
