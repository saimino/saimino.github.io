---
title: "머신러닝 수학 주차별 로드맵"
date: "2026-11-14"
tags:
  - type/concept
  - math
---

일반적인 머신러닝 수업 목차를 따라가며, 주차마다 개념과 핵심 수식을 정리하는 시리즈의 목차입니다. 수업 한 학기 분량 14주차 뒤에 딥러닝 모델(MLP, CNN, RNN, 트랜스포머, 디퓨전) 5주차를 더해 모두 19주차입니다. 시험 주차는 뺐습니다.

## 글 형식

각 주차 글은 같은 순서로 씁니다.

1. 한 줄 정의: 이 주차의 개념이 무엇을 푸는지 한 문장으로 적습니다.
2. 표기: 글에서 쓰는 기호를 먼저 정합니다.
3. 핵심 수식: 결과 식을 먼저 보여주고, 유도를 단계별로 적습니다.
4. 해석: 식의 각 항이 무슨 뜻인지 풀어서 적습니다.
5. 연결: 앞뒤 주차의 어떤 식과 이어지는지 적습니다.

기호의 뜻과 그 기호를 쓰는 이유(합, 로그, 기댓값 등)는 처음 나오는 주차에서 자세히 설명합니다. 두 번쯤 설명한 뒤에는 중요한 경우가 아니면 생략합니다.

공통 표기는 다음과 같습니다. 데이터는 $\mathcal{D} = \{(x_i, y_i)\}_{i=1}^{n}$, 입력은 $x_i \in \mathbb{R}^d$, 설계 행렬은 $X \in \mathbb{R}^{n \times d}$, 파라미터는 $\theta$ 또는 $w$입니다.

## 1부: 기초 수학

### 1주차: 머신러닝 문제 정의

- 글: [[머신러닝 문제 정의]]
- 개념: 지도 학습과 비지도 학습, 가설 공간, 손실 함수, 경험적 위험 최소화, 일반화
- 핵심 수식

$$
R(f) = \mathbb{E}_{(x, y) \sim p}\left[\ell(f(x), y)\right], \qquad
\hat{\theta} = \arg\min_{\theta} \frac{1}{n} \sum_{i=1}^{n} \ell(f_\theta(x_i), y_i)
$$

- 기존 노트: [[ML Basics Intro]]

### 2주차: 선형대수

- 글: [[선형대수]]
- 개념: 내적과 노름, 선형 독립과 랭크, 고유값 분해, 특이값 분해, 양의 정부호 행렬, 행렬 미분
- 핵심 수식

$$
A = U \Sigma V^\top, \qquad
\nabla_x \left(x^\top A x\right) = (A + A^\top) x, \qquad
\nabla_x \lVert Ax - b \rVert_2^2 = 2 A^\top (Ax - b)
$$

- 기존 노트: [[Matrix 1]], [[Matrix 2]], [[Span Basis벡터 Dimension (Linear Independence)과 편미분]], [[벡터의 유사도 계산 (Norm 등)방법들]], [[Derivative]]

### 3주차: 확률과 통계

- 글: [[확률과 통계]]
- 개념: 조건부 확률과 베이즈 정리, 기댓값과 분산, 공분산, 가우시안 분포, 최대우도추정(MLE), 최대사후확률추정(MAP)
- 핵심 수식

$$
p(\theta \mid \mathcal{D}) = \frac{p(\mathcal{D} \mid \theta)\, p(\theta)}{p(\mathcal{D})}, \qquad
\hat{\theta}_{\text{MLE}} = \arg\max_{\theta} \sum_{i=1}^{n} \log p(x_i \mid \theta)
$$

$$
\mathcal{N}(x \mid \mu, \Sigma) = \frac{1}{(2\pi)^{d/2} \lvert \Sigma \rvert^{1/2}} \exp\left(-\frac{1}{2} (x - \mu)^\top \Sigma^{-1} (x - \mu)\right)
$$

- 기존 노트: [[Probability]], [[Bayes Rule]], [[Distance Measure]]

## 2부: 지도 학습

### 4주차: 선형 회귀

- 글: [[선형 회귀]]
- 개념: 최소제곱법, 정규방정식, 열공간으로의 사영, 가우시안 노이즈 가정에서 MLE와 최소제곱이 같아지는 이유
- 핵심 수식

$$
J(w) = \frac{1}{2} \lVert Xw - y \rVert_2^2, \qquad
\nabla_w J = X^\top (Xw - y) = 0 \;\Rightarrow\; w^* = (X^\top X)^{-1} X^\top y
$$

- 기존 노트: [[Regression]], [[평균제곱오차(MSE), 평균절대오차(MAE)]]

### 5주차: 최적화

- 글: [[최적화]]
- 개념: 경사하강법, 볼록 함수, 학습률과 수렴, 확률적 경사하강법(SGD), 모멘텀, 뉴턴법
- 핵심 수식

$$
\theta_{t+1} = \theta_t - \eta \nabla J(\theta_t), \qquad
\theta_{t+1} = \theta_t - H^{-1} \nabla J(\theta_t)
$$

$$
f(\lambda x + (1 - \lambda) y) \le \lambda f(x) + (1 - \lambda) f(y), \quad \lambda \in [0, 1]
$$

### 6주차: 규제와 편향 분산

- 글: [[규제와 편향 분산]]
- 개념: 과적합, Ridge와 Lasso, 규제를 사전분포(MAP)로 보는 해석, 편향 분산 분해, 교차 검증
- 핵심 수식

$$
w_{\text{ridge}} = \arg\min_{w} \lVert Xw - y \rVert_2^2 + \lambda \lVert w \rVert_2^2 = (X^\top X + \lambda I)^{-1} X^\top y
$$

$$
\mathbb{E}\left[(y - \hat{f}(x))^2\right] = \left(\mathbb{E}[\hat{f}(x)] - f(x)\right)^2 + \mathrm{Var}[\hat{f}(x)] + \sigma^2
$$

### 7주차: 로지스틱 회귀

- 글: [[로지스틱 회귀]]
- 개념: 시그모이드, 베르누이 분포의 MLE, 교차 엔트로피 손실, 소프트맥스와 다중 분류
- 핵심 수식

$$
\sigma(z) = \frac{1}{1 + e^{-z}}, \qquad
L(w) = -\sum_{i=1}^{n} \left[ y_i \log \hat{y}_i + (1 - y_i) \log (1 - \hat{y}_i) \right], \qquad
\nabla_w L = X^\top (\hat{y} - y)
$$

$$
\mathrm{softmax}(z)_k = \frac{e^{z_k}}{\sum_{j} e^{z_j}}
$$

- 기존 노트: [[Euler's Number]]

### 8주차: 생성 모델 분류기와 평가 지표

- 글: [[생성 모델 분류기와 평가 지표]]
- 개념: 판별 모델과 생성 모델의 차이, 가우시안 판별 분석(GDA), 나이브 베이즈, 정밀도와 재현율, F1, ROC
- 핵심 수식

$$
p(y \mid x) \propto p(x \mid y)\, p(y), \qquad
p(x \mid y) = \prod_{j=1}^{d} p(x_j \mid y)
$$

$$
\text{Precision} = \frac{TP}{TP + FP}, \qquad
\text{Recall} = \frac{TP}{TP + FN}, \qquad
F_1 = \frac{2 \cdot \text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
$$

- 기존 노트: [[Classification]]

### 9주차: 서포트 벡터 머신

- 글: [[서포트 벡터 머신]]
- 개념: 마진 최대화, 라그랑주 승수법과 쌍대 문제, KKT 조건, 소프트 마진, 힌지 손실
- 핵심 수식

$$
\min_{w, b} \frac{1}{2} \lVert w \rVert_2^2 \quad \text{s.t.} \quad y_i (w^\top x_i + b) \ge 1
$$

$$
\max_{\alpha} \sum_{i} \alpha_i - \frac{1}{2} \sum_{i, j} \alpha_i \alpha_j y_i y_j x_i^\top x_j \quad \text{s.t.} \quad \alpha_i \ge 0, \; \sum_{i} \alpha_i y_i = 0
$$

### 10주차: 커널 방법

- 글: [[커널 방법]]
- 개념: 특징 사상, 커널 트릭, RBF 커널, 머서 조건, 커널 릿지 회귀
- 핵심 수식

$$
k(x, x') = \phi(x)^\top \phi(x'), \qquad
k_{\text{RBF}}(x, x') = \exp\left(-\frac{\lVert x - x' \rVert_2^2}{2\sigma^2}\right), \qquad
f(x) = \sum_{i=1}^{n} \alpha_i k(x_i, x)
$$

### 11주차: 결정 트리와 앙상블

- 글: [[결정 트리와 앙상블]]
- 개념: 엔트로피와 정보 이득, 지니 불순도, 배깅과 랜덤 포레스트, AdaBoost, 그래디언트 부스팅
- 핵심 수식

$$
H(S) = -\sum_{k} p_k \log_2 p_k, \qquad
IG(S, A) = H(S) - \sum_{v} \frac{\lvert S_v \rvert}{\lvert S \rvert} H(S_v), \qquad
\alpha_t = \frac{1}{2} \ln \frac{1 - \epsilon_t}{\epsilon_t}
$$

## 3부: 비지도 학습과 이론

### 12주차: 차원 축소

- 글: [[차원 축소]]
- 개념: 주성분 분석(PCA), 분산 최대화와 복원 오차 최소화, 공분산 행렬의 고유값 분해, SVD와의 관계
- 핵심 수식

$$
S = \frac{1}{n} \sum_{i=1}^{n} (x_i - \bar{x})(x_i - \bar{x})^\top, \qquad
\max_{\lVert u \rVert_2 = 1} u^\top S u \;\Rightarrow\; S u = \lambda u
$$

- 기존 노트: [[PCA]]

### 13주차: 군집과 EM 알고리즘

- 글: [[군집과 EM 알고리즘]]
- 개념: k-means, 가우시안 혼합 모델(GMM), 잠재 변수, EM 알고리즘, ELBO
- 핵심 수식

$$
J = \sum_{i=1}^{n} \sum_{k=1}^{K} r_{ik} \lVert x_i - \mu_k \rVert_2^2, \qquad
\gamma_{ik} = \frac{\pi_k\, \mathcal{N}(x_i \mid \mu_k, \Sigma_k)}{\sum_{j} \pi_j\, \mathcal{N}(x_i \mid \mu_j, \Sigma_j)}
$$

$$
\log p(x) \ge \mathbb{E}_{q(z)}\left[\log p(x, z)\right] - \mathbb{E}_{q(z)}\left[\log q(z)\right]
$$

### 14주차: 정보 이론과 학습 이론

- 글: [[정보 이론과 학습 이론]]
- 개념: 엔트로피, KL 발산, 교차 엔트로피와 MLE의 관계, PAC 학습, VC 차원, 일반화 경계
- 핵심 수식

$$
D_{\text{KL}}(p \,\Vert\, q) = \sum_{x} p(x) \log \frac{p(x)}{q(x)}, \qquad
H(p, q) = H(p) + D_{\text{KL}}(p \,\Vert\, q)
$$

$$
P\left(\lvert \hat{R}(f) - R(f) \rvert \gt \epsilon\right) \le 2 e^{-2 n \epsilon^2}
$$

## 4부: 딥러닝 모델

### 15주차: MLP와 역전파

- 글: [[MLP와 역전파]]
- 개념: 퍼셉트론, 활성화 함수, 순전파, 연쇄 법칙, 역전파, 보편 근사 정리
- 핵심 수식

$$
z^{(l)} = W^{(l)} a^{(l-1)} + b^{(l)}, \qquad a^{(l)} = \sigma(z^{(l)})
$$

$$
\delta^{(l)} = \left(W^{(l+1)\top} \delta^{(l+1)}\right) \odot \sigma'(z^{(l)}), \qquad
\frac{\partial \ell}{\partial W^{(l)}} = \delta^{(l)} a^{(l-1)\top}
$$

### 16주차: CNN

- 글: [[CNN]]
- 개념: 합성곱 연산, 파라미터 공유, 패딩과 스트라이드, 풀링, 수용 영역, 평행이동 등변성
- 핵심 수식

$$
(X * K)_{i, j} = \sum_{m} \sum_{n} X_{i+m,\, j+n}\, K_{m, n}, \qquad
O = \left\lfloor \frac{I - K + 2P}{S} \right\rfloor + 1
$$

### 17주차: RNN

- 글: [[RNN]]
- 개념: 은닉 상태와 순환식, 시간에 걸친 가중치 공유, 시간에 따른 역전파(BPTT), 기울기 소실과 폭발, LSTM
- 핵심 수식

$$
h_t = \tanh\left(W_h h_{t-1} + W_x x_t + b\right), \qquad
\frac{\partial h_t}{\partial h_k} = \prod_{j=k+1}^{t} \mathrm{diag}\left(1 - h_j^2\right) W_h
$$

$$
c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t, \qquad h_t = o_t \odot \tanh\left(c_t\right)
$$

### 18주차: 트랜스포머

- 글: [[트랜스포머]]
- 개념: 셀프 어텐션, 스케일드 닷 프로덕트 어텐션, 멀티 헤드 어텐션, 위치 인코딩, 잔차 연결과 층 정규화
- 핵심 수식

$$
\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V
$$

$$
PE_{(pos,\, 2i)} = \sin\left(\frac{pos}{10000^{2i / d}}\right), \qquad
PE_{(pos,\, 2i+1)} = \cos\left(\frac{pos}{10000^{2i / d}}\right)
$$

- 기존 노트: [[Attention Is All You Need (Attention Mechanism & Transformers)]], [[Transformer to Qwen3 Architecture Evolution]]

### 19주차: 디퓨전 모델

- 글: [[디퓨전 모델]]
- 개념: 순방향 과정과 역방향 과정, 노이즈 스케줄, 임의 시점의 닫힌 형태, ELBO에서 노이즈 예측 손실로의 단순화, 스코어 함수와의 관계
- 핵심 수식

$$
q(x_t \mid x_{t-1}) = \mathcal{N}\left(x_t \mid \sqrt{1 - \beta_t}\, x_{t-1},\, \beta_t I\right), \qquad
x_t = \sqrt{\bar{\alpha}_t}\, x_0 + \sqrt{1 - \bar{\alpha}_t}\, \epsilon, \quad \bar{\alpha}_t = \prod_{s=1}^{t} (1 - \beta_s)
$$

$$
L_{\text{simple}} = \mathbb{E}_{t, x_0, \epsilon}\left[\lVert \epsilon - \epsilon_\theta(x_t, t) \rVert_2^2\right]
$$
