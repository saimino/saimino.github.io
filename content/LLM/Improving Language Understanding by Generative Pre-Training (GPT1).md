---
title: "Improving Language Understanding by Generative Pre-Training (GPT1)"
date: "2024-08-10"
tags: ["type/paper"]
aliases: ["tistory-37"]
source: "https://choimino.tistory.com/37"
---

paper : <https://www.cs.ubc.ca/~amuham01/LING530/papers/radford2018improving.pdf>

model : <https://huggingface.co/openai-community/openai-gpt>

> [openai-community/openai-gpt · Hugging Face](https://huggingface.co/openai-community/openai-gpt)  
> huggingface.co

이 논문은 NLP분야에서 센세이션했었던 GPT 34의 토대가 되는 GPT1에 대한 논문이다.

### Introduction

대부분의 딥러닝 방법은 수동으로 레이블을 붙인 대량의 레이블링 데이터가 필요하고, 비용이 많이 든다.  
또한, 원시 텍스트로부터 효과적으로 학습하는 능력은 자연어 처리(NLP)에서 지도 학습에 대한 의존성을 완화하는 데 매우 중요하다고 한다.

대부분의 딥 러닝 방법에는 상당한 양의 수동으로 레이블이 지정된 데이터가 필요하므로 주석이 달린 리소스가 부족한 많은 도메인에서의 적용 가능성이 제한된다.

자연어는 라벨링이 되지 않은 데이터들이 많지만, 학습하기 위한 라벨링된 데이터는 충분하지 않다는 문제가 있었다.

Raw 텍스트로 학습하는 건 자연어 처리에서 지도 학습에 대한 의존성을 완화하는 데 매우 중요하다고 한다.

그래서 이 논문에서 제안 한 방법은 비지도 학습과 미세 조정으로 조합을 해서 언어 모델을 연구했고, **(1)대규모의 언라벨링 텍스트 코퍼스 에서의 비지도 사전학습**과 **(2)다운 스트림 테스크에 대한 지도 학습을 파인튜닝**을 통한 기존 학습방법보다 더 좋은 방법을 제시한다.

### Architecture

아키텍쳐는 아시다시피 요즘 다 유명하고,  기능이 강력한 LLM들은 GPT1에서 제안한 decoder-only구조로 사용한다:

![[37-bc863e28c6.png]]

인풋 엑스가 주어지면 위치에 대해 임베딩 메트릭스와 곱해주고, 각 위치정보를 가지고 있는 포지션 메트릭스를 더해주어,  마스크드 멀티헤드 어텐션 을 거치게 된다. 트랜스포머 블록이 여러개 처리를 하게되고 최종적으로 가장 마지막 히든 스테이트와 임베딩 메트릭스의 소프트맥스를 취해서 각 토큰들의 아웃풋 값을 얻게 된다.  
  
트랜스포머와 비교하자면, 트랜스포머에서 디코더만 가져왔고, cross attention을 제거한 것을 볼 수가 있는데, encoder를 사용하지 않았기 때문에, encoder의 결과를 합쳐주는 cross-attention이 필요없다.  
인코더를 제외하고 디코더만 사용하는 이유는 그 전 단어를 보고, 다음 단어를 예측하는 방법을 사용하여 학습을 하기때문에, decoder만 사용한다. 이 논문에서는 디코더를 12개 쌓은 구조를 하고 있다.

### Pre-Training

GPT-1의 Unsupervised Pre-Training 방법을 살펴보면, 앞서 언급한대로 GPT-1 논문의 핵심이라고 할 수 있다. GPT-1부터 시작해서 GPT-2, GPT-3, InstructGPT, 그리고 ChatGPT까지 이어지는 GPT 시리즈의 공통된 학습 철학이라고 할 수 있다.

방법은 간단한데, GPT-1은 위에서 잠깐 언급했듯이 다음 단어를 맞추도록 학습한다. 논문에서는 Next Word Prediction이라고 표현하는데, 수식으로는 간단하게 표현된다:

$$
L_1(\mathcal{U}) = \sum_i \log P(u_i \mid u_{i-k}, \ldots, u_{i-1}; \Theta)
$$

unsupervized copus에 대해 window size k개의 token이 주어졌을 때 next token을 예측하고 그 likelihood를 최대화 하도록 학습 하는 것이 unsupervized leaning이다.

조금 더 구체적으로 보면, 전체 데이터셋은 아주 많은 문장으로 구성되어 있을텐데, 이 데이터셋을 문장별로 나누어준다. 그리고 각 문장을 GPT-1에 입력해주는데, 문장을 잘라서 주고 그 다음에 나올 단어를 예측하도록 학습하는것이다. 예를 들어 ‘**Time flies like an arrow**’ 라는 문장이 데이터셋에 있다고 가정해보면, 이때 GPT-1에게 ‘**Time**’ 이라는 단어를을 입력해주고, 12개의 decoder를 거쳐서 나온 아웃풋 벡터와 토큰임베딩 트렌스포즈한 것을 곱했을때, 아웃풋 토큰들의 확률이 나오게 된다. 다음과 같이 모든 토큰중에 가장 높은 값인 플라이 라는 말을 출력하게 됩니다. 이렇게 다음에 나올 단어를 예측하도록 학습하는거라고 볼 수 있다.

![[37-b8fb155828.png]]

출처 : https://mr-waguwagu.tistory.com/27

또한 BERT 등 다른 LLM들과 차별화되는 방법이며 근본적인 성능 차이를 가져오는 원인중 하나라고 할 수 있다.

### Fine-Tuning

그 다음 과정으로는 Pre-trained model을 fine-tune 하는 과정이다.

이렇게 Pre-Training을 마친 모델은 최종 성능 측정을 하기에 앞서 각 Task에 맞도록 재학습을 하고, 이 과정을 Fine Tuning이라고 하는데, 이러한 Fine Tuning은 앞선 Pre-Training과 달리 Supervised Learning 방법으로 이루어진다. Fine Tuning을 위한 데이터셋은 Labeled Dataset으로 구성되어 있기 때문이죠. 따라서 Loss 함수는 다음과 같이 간단하게 표현된다.

$$
L_2(\mathcal{C}) = \sum_{(x, y)} \log P(y \mid x^1, \ldots, x^m)
$$

Pre-trained model의 Loss를 L1 으로하고, Fine-tune의 Loss를 L2 로 둬서 두개의 로스를 동시에 사용하여 최종 Loss를 도출한다.

$$
L_3(\mathcal{C}) = L_2(\mathcal{C}) + \lambda \ast L_1(\mathcal{C})
$$

람다는 스케일러이다.

그럼 "Task 별로 Fine Tuning을 할때 Input Data는 어떻게 구성해줄까?" 라는 의문이 생긴다. 예를 들어 하나의 문장의 종류를 구분하는 Classification 문제와, 두개의 문장을 입력받아 유사도를 측정하는 Similarity 문제에서의 Input Data 구성만 다르고 다른 트랜스포머를 거치고, 파인튜닝하는 리니어를 거치면 각 다운 스트림 테스크에 대한 것을 학습할 수 있게 된다.

여기서 gpt1 의 단점이 나오게 되는데, 파인튜닝을 필수로 해야한다는 단점이 있다. introduction에서 언급했었던, 라벨링 되지 않은 데이터로 비지도 학습을 할 수 있다는 장점이 fine tune을 위한 지도 학습때문에 장점이 퇴색 된다는 단점이 있었다.

나중에 글을 작성하겠지만, gpt2이후 모델 부터는 학습데이터와 모델 사이즈를 획기적으로 올려 비지도 학습으로  충분한 성능을 나올 수 있게 구축을 했다.

아래는 fine tuning을 하는 tesk들의 대표적인 예시이다.

![[37-87a8eeb465.png]]

대표적인 Task들을 하나씩 살펴보자면,

먼저 Classification 문제인데, 이는 입력받은 Text를 분류하는 문제이다. 가장 대표적으로 스팸 메일 분류 문제가 있다. 메일 내용 전체를 입력으로 주고 모델은 이 메일이 스팸인지 아닌지를 구분하는 문제이다. 이때는 단순히 문장 전체를 모델에 입력으로 넣어주면 된다.  
그 외 tesk를 간단히 설명하면,  
Textual Entailment는 2개의 문장을 입력 받아 두 문장의 관계를 Classification 하는 문제이다.  
Similarity는 두개의 문장을 입력 받아 두 문장이 얼마나 유사한지를 측정하는 문제이다.  
Multiple Choice는 여러개의 선택지 중에서 하나를 결정하는 문제이다.

이 논문에서는 이 각각의 tesk들(위 4개에 국한되지 않음)의 fine tuning 을 해서 성능을 올리는 방법으로 학습을 진행했다.

### Result

![[37-590be5fff7.png]]

![[37-9c5f3c0487.png]]

결과는 논문 참조
