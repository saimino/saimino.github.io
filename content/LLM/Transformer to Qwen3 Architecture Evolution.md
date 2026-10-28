---
tags:
  - type/concept
  - ai/llm
---

# Transformer to Qwen3 Architecture Evolution

기본 Transformer에서 Qwen3까지 구조가 어떻게 바뀌었는지 정리한 노트입니다. 순수 아키텍처, 어텐션, FFN, 포지션, 스케일링, 학습 안정화까지 다룹니다.

관련 노트는 [[LLM Glossary]], [[LLM Tech Stack]], [[LoRA]], [[QLoRA]], [[LLAMA2]]입니다.

## 0. 기준점: 기본 Transformer

Vaswani et al. (2017) 기준 구조입니다. 아래 항목들이 이후 세대에서 무엇으로 대체됐는지가 이 노트의 내용입니다.

| 기본 Transformer | 현재 세대 |
| --- | --- |
| Absolute positional embedding | RoPE |
| Dense FFN (ReLU) | SwiGLU, 그리고 MoE |
| Full self attention (MHA) | GQA |
| LayerNorm | RMSNorm |
| Post-LN | Pre-LN |
| 고정 컨텍스트 길이 | YaRN 등으로 확장 |
| Dense parameter activation | Sparse activation (MoE) |

## 1. Position Encoding

### 1.0 왜 위치 정보가 필요한가

```
개가 사람을 물었다.
사람이 개를 물었다.
```

두 문장은 단어 집합이 같고 순서만 다르지만 뜻이 정반대입니다. 그런데 어텐션은 모든 토큰 쌍의 유사도를 동시에 계산하기 때문에 순서 자체를 볼 수 없습니다. 그래서 위치 정보를 따로 넣어줘야 합니다.

**1세대: Absolute Positional Embedding**

위치마다 고정된 벡터를 만들어 입력 임베딩에 더합니다.

$$x_i = e_i + p_i$$

이 $x_i$가 그대로 어텐션 계산에 들어갑니다. 문제는 의미 정보 $e_i$와 위치 정보 $p_i$가 **덧셈으로 섞여버린다**는 점입니다. 성격이 완전히 다른 두 정보인데 구조적으로 분리되지 않습니다. 또 학습 때 본 길이를 넘어가면 해당 위치의 $p_i$가 없어서 외삽이 안 됩니다.

**2세대: Relative Position Bias**

절대 위치 대신 두 토큰의 상대 거리를 씁니다. 어텐션 스코어에 거리 기반 편향을 더해서 가까우면 세밀하게, 멀면 약하게 보도록 만듭니다. T5의 relative position bias, ALiBi가 이 계열입니다.

$$\text{score}_{ij} = \frac{q_i^\top k_j}{\sqrt{d}} + b_{i-j}$$

의미와 위치가 섞이는 문제는 풀리지만, 어텐션 스코어를 구한 뒤에 **매번 별도 연산을 한 번 더** 얹어야 합니다. 시퀀스가 길어지면 이 비용이 그대로 따라 커집니다.

### 1.1 RoPE (Rotary Positional Embedding)

핵심 아이디어는 **더하지 말고 회전시키자**입니다.

복소수 지수함수 $e^{i\theta}$는 크기가 항상 1입니다. 즉 벡터에 곱하면 **길이는 그대로 두고 각도만 돌립니다**. 의미 정보(벡터의 크기와 방향)를 훼손하지 않고 위치 정보(회전각)만 얹을 수 있다는 뜻입니다.

위치 $m$의 쿼리와 위치 $n$의 키를 각각 $m\theta$, $n\theta$만큼 회전시킵니다.

$$f(q, m) = q\,e^{im\theta}, \qquad f(k, n) = k\,e^{in\theta}$$

둘의 내적을 구하면 이렇게 됩니다.

$$\langle f(q,m),\, f(k,n) \rangle = \mathrm{Re}\left[q\,\bar{k}\,e^{i(m-n)\theta}\right]$$

결과가 $m-n$, 즉 **상대 거리에만 의존**합니다. 절대 위치를 넣었는데 상대 위치가 자동으로 나옵니다.

RoPE가 앞선 두 방식보다 나은 점입니다.

- 위치 정보가 Q와 K의 **회전에 직접 반영**되므로 어텐션 스코어에 별도 항을 더할 필요가 없습니다
- 의미와 위치가 덧셈으로 섞이지 않습니다
- 학습 길이를 넘는 위치에도 회전각을 계속 돌리면 되므로 외삽이 가능합니다

실제로는 임베딩 차원을 2개씩 짝지어 2차원 회전행렬을 적용하고, 짝마다 다른 주파수를 씁니다.

$$\theta_j = 10000^{-2j/d}$$

낮은 차원은 빠르게 회전해 가까운 거리를, 높은 차원은 천천히 회전해 먼 거리를 구분합니다. 음악에서 절대 음높이보다 **음 사이의 간격이 멜로디를 만드는 것**과 같은 구조입니다. 조를 옮겨도(전체를 회전시켜도) 멜로디는 유지됩니다.

### 1.2 RoPE 스케일링으로 컨텍스트 확장

학습 길이를 넘어가면 회전각이 학습 중 본 적 없는 영역으로 들어가 성능이 떨어집니다. 그래서 주파수 $\theta_j$를 조정해 긴 입력을 학습 범위 안으로 밀어 넣습니다.

| 방식 | 내용 |
| --- | --- |
| Position Interpolation | 위치 인덱스를 일괄 축소합니다. 단순하지만 고주파 정보가 뭉갭니다 |
| NTK-aware scaling | 저주파는 크게, 고주파는 거의 그대로 두어 세밀한 위치 구분을 지킵니다 |
| YaRN | NTK 계열을 개선한 방식으로, 주파수 대역별로 다르게 처리하고 어텐션 온도도 함께 보정합니다 |

Qwen 계열은 Qwen2에서 긴 컨텍스트 처리를 본격적으로 다듬었고, Qwen3는 네이티브 32k에 YaRN을 적용해 131k까지 확장합니다. 여기에 Dual Chunk Attention을 함께 씁니다.

주의할 점은 이 확장이 **자동이 아니라 설정으로 켜는 방식**이라는 것입니다. 짧은 입력에 켜두면 오히려 성능이 떨어질 수 있어서, 긴 입력을 실제로 다룰 때만 켜는 게 맞습니다.

## 2. Attention 구조

### 2.1 GQA (Grouped Query Attention)

추론할 때 병목은 연산량이 아니라 **KV cache 메모리**입니다. 캐시 크기는 KV head 수에 비례해서 커집니다.

| 방식 | KV head 수 | 특징 |
| --- | --- | --- |
| MHA | Q head와 동일 | 품질 최고, 캐시 최대 |
| MQA | 1개 | 캐시 최소, 품질 손실 |
| GQA | Q head를 그룹으로 묶어 그룹당 1개 | 둘 사이의 절충 |

Qwen3는 전 모델에서 GQA를 씁니다. 긴 컨텍스트를 실사용 가능하게 만든 핵심 요소입니다.

### 2.2 QK-Norm

깊은 모델을 큰 배치로 학습하면 어텐션 로짓 $q^\top k$가 폭주해서 softmax가 포화되고 학습이 불안정해집니다. Qwen3는 Q와 K에 각각 RMSNorm을 적용해 이를 막습니다. 동시에 Qwen2에 있던 **QKV bias를 제거**했습니다.

### 2.3 Hybrid Attention

일부 레이어는 full attention, 일부는 windowed 또는 선형 어텐션을 써서 긴 문맥과 국소 정보를 동시에 잡는 방식입니다. 다만 이건 Qwen3 본체가 아니라 **Qwen3-Next 계열의 특징**입니다. 자세한 건 아래 9번을 봅니다.

## 3. FFN 구조

### 3.1 SwiGLU

ReLU FFN을 걷어내고 게이팅 구조를 씁니다.

$$\text{SwiGLU}(x) = \big(\text{Swish}(xW_1) \odot xW_3\big)W_2$$

한쪽 경로가 게이트 역할을 해서 어떤 정보를 통과시킬지 조절합니다. 행렬이 2개에서 3개로 늘어나는 대신 중간 차원을 줄여 파라미터 수를 맞추는데, 그렇게 해도 표현력이 더 좋습니다. LLaMA 이후 사실상 표준입니다.

### 3.2 MoE (Mixture of Experts)

Qwen3의 가장 큰 구조 변화입니다. Dense FFN 하나를 여러 expert로 쪼개고, 토큰마다 일부만 켭니다.

구성 요소입니다.

1. **Router**: 토큰별로 어떤 expert를 쓸지 점수를 냅니다
2. **Top-k selection**: 점수 상위 k개만 활성화합니다
3. **Load balancing loss**: 특정 expert로 쏠리는 것을 막습니다

효과는 **전체 용량과 연산량의 분리**입니다. 모델이 담는 지식의 총량은 전체 파라미터를 따라가지만, 토큰 하나를 처리할 때의 비용은 활성 파라미터만 따라갑니다.

Qwen3 MoE의 구성입니다.

- expert 128개 중 토큰당 8개 활성화
- **shared expert 없음**. Qwen2.5-MoE에는 있었는데 Qwen3에서 뺐습니다
- global batch 단위 load balancing loss를 씁니다

예를 들어 Qwen3-30B-A3B는 총 30B 파라미터에 활성 3B입니다. 30B급 지식을 담으면서 추론 비용은 3B급입니다.

## 4. Normalization

### 4.1 RMSNorm

LayerNorm에서 평균 빼는 연산을 없애고 분산 기반 스케일링만 남깁니다.

$$\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum x_i^2 + \epsilon}} \cdot g$$

평균 계산과 shift 파라미터가 사라져 연산이 줄고, 실제로 성능 손실이 거의 없습니다. 대규모 모델에서 수렴도 더 안정적입니다.

### 4.2 Pre-Norm 고정

정규화를 서브레이어 **앞에** 둡니다. 이렇게 하면 residual 경로가 정규화를 거치지 않고 그대로 이어져서, 레이어가 수십 개로 깊어져도 gradient가 살아서 내려옵니다. Post-LN은 깊어지면 warmup 없이는 학습이 안 됩니다.

## 5. Scaling

### 5.1 Scaling law 반영

파라미터만 늘리는 게 아니라 depth, width, expert 수, 학습 토큰 수를 함께 맞춥니다. Chinchilla 이후로는 **주어진 연산 예산에서 모델 크기와 데이터 양의 비율**을 맞추는 게 기본이 됐습니다.

### 5.2 Token-efficient training

데이터의 질로 승부하는 방향입니다. Qwen3는 사전학습 토큰을 약 36T로 늘렸고(Qwen2.5는 18T) 119개 언어를 다룹니다. 단순 웹 텍스트 비중을 줄이고 수학, 코딩, 합성 데이터 비중을 올렸습니다. [[Overfitting]]과도 맞닿는 부분으로, 같은 토큰을 반복해 보는 것보다 새로운 고품질 토큰이 낫습니다.

## 6. Long Context 학습 전략

### 6.1 Chunked attention training

긴 시퀀스를 chunk 단위로 끊어 학습합니다. 어텐션 메모리는 길이의 제곱에 비례하므로 통째로 넣으면 OOM이 납니다.

### 6.2 Context curriculum

처음부터 긴 컨텍스트로 학습하지 않고 단계적으로 늘립니다.

```
4k → 32k → (YaRN) → 128k
```

짧은 구간에서 언어 능력을 먼저 확보하고, 마지막 단계에서 긴 컨텍스트에 적응시킵니다. 처음부터 길게 가면 연산 낭비가 크고 학습도 불안정합니다.

## 7. MoE 라우팅 안정화

### 7.1 Load balancing

라우터를 그냥 두면 소수 expert로 토큰이 쏠리고 나머지는 **dead expert**가 됩니다. 학습이 될수록 잘 뽑히는 expert가 더 좋아지는 양의 되먹임이 생기기 때문입니다. 이를 막으려고 보조 손실(auxiliary loss)을 더해서 expert 사용 분포를 고르게 만듭니다.

Qwen3는 배치 단위가 아니라 **global batch 단위**로 균형을 잡습니다.

### 7.2 라우팅 다양성 확보

학습 초반 라우터에 노이즈를 넣어 특정 expert 고착을 막는 기법도 있습니다. 다만 이건 Switch Transformer 계열 초기 MoE 연구의 기법이고, Qwen3가 쓴다고 확인되진 않았습니다.

## 8. 추론 최적화

### 8.1 KV cache 축소

GQA 덕분에 KV head가 줄어 캐시가 그만큼 작아집니다. 128k 컨텍스트를 실제로 돌릴 수 있게 만든 직접적인 요인입니다.

### 8.2 Thinking budget

Qwen3는 thinking mode와 non-thinking mode를 한 모델에 넣고, 추론 토큰 예산을 조절할 수 있게 했습니다. 아키텍처 변경은 아니고 post-training과 추론 제어 쪽 변화지만 사용 관점에서는 가장 눈에 띄는 차이입니다.

## 9. 확인이 필요한 항목

원본 정리에서 Qwen3 본체와 어긋나거나 출처가 불분명한 부분입니다. 시험이나 발표에 쓸 거면 여기부터 확인합니다.

| 항목 | 문제 | 정확한 서술 |
| --- | --- | --- |
| Hybrid attention | Qwen3 본체는 모든 레이어가 full attention(GQA)입니다 | 선형 어텐션 혼합은 Qwen3-Next의 특징입니다. Gated DeltaNet과 gated attention을 3:1로 섞습니다. Qwen2 일부 모델에는 SWA가 있었습니다 |
| Attention logit 안정화 | "softmax 이전 스케일링 조정"은 모호합니다 | QK-Norm으로 적는 게 정확합니다. Q와 K에 RMSNorm 적용, QKV bias 제거입니다 |
| Dynamic RoPE scaling | 추론 시 자동으로 바뀌지 않습니다 | YaRN과 Dual Chunk Attention을 설정으로 켜는 방식입니다 |
| Logit clipping | Qwen3 문서에서 확인되지 않습니다 | 일반적인 추론 안정화 기법이지 Qwen3 고유 요소가 아닙니다 |
| Router noise injection | Qwen3 적용 여부가 불분명합니다 | Qwen3가 명시한 건 global batch load balancing loss입니다 |

## 10. 한 장 요약

기본 Transformer에서 Qwen3까지의 변화를 한 줄로 줄이면 이렇습니다.

> **위치는 더하지 말고 돌리고(RoPE), 캐시는 줄이고(GQA), FFN은 게이팅으로 바꾸고(SwiGLU), 필요한 부분만 켜고(MoE), 정규화는 가볍게 앞에 두고(Pre-RMSNorm), 컨텍스트는 단계적으로 늘린다(curriculum + YaRN).**

각 변화가 노린 것을 분류하면 이렇습니다.

| 목적 | 해당 기법 |
| --- | --- |
| 표현력 | RoPE, SwiGLU, MoE |
| 메모리 | GQA, KV cache 최적화 |
| 학습 안정성 | RMSNorm, Pre-LN, QK-Norm, load balancing loss |
| 길이 확장 | YaRN, DCA, context curriculum, chunked training |

## 남은 정리 항목

- [ ] YaRN 논문 읽고 별도 노트로 분리하기
- [ ] MoE router 수식 직접 정리하기
- [ ] Qwen3-Next의 Gated DeltaNet 구조 확인하기
- [ ] 9번 표의 항목들 Qwen3 technical report로 대조하기
