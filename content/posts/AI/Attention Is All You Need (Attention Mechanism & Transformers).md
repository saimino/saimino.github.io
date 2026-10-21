---
title: "Attention Is All You Need (Attention Mechanism & Transformers)"
date: "2024-08-05"
tags: ["AI"]
aliases: ["tistory-34"]
source: "https://choimino.tistory.com/34"
---

**Previous Knowledge :**  
**RNN**은 순차적으로 하나씩 시퀀스로 인풋으로 읽어온다. 읽어오면서 자기자신을 덮어 씌워주면서 업데이트를 하는 방식으로써, CNN같은 인풋 길이를 고정적으로 정하지 않고 입력에 따라 반복하여 넣어줌으로써 가변적인 인풋을 받을 수 있게됐다. **RNN**은 기본적으로 fully connect layer 를 계속 통과하기 때문에, Backpropagation 시에 미분값이 계속 곱해져서 Gradient Venising 이나 Gradient Exploding 문제가 있을 수 있고, 긴 데이터를 잘 기억하지 못하는 문제가 있다.  LSTM은 sell state 라는 장기기억장치를 추가해주고 숏컷를 추가하여 해결

**many to many**(복수개의 입력, 복수개의 출력)에서, 하나의 입력에 하나의 출력을 하게 되면 전체적인 맥락을 보지 못하고 출력을 하게되어 문제가 있었다. 그래서, **encoder-decoder** 구조를 사용하여 전체적인 입력을 다 보고 난 다음에 출력을 하게하는 방식으로 처리했다.

![[34-9e972e4c58.jpg]]

Encoder Decoder RNN 구조

### Attention

위에서 말했던 encoder-decorder 구조를 사용하더라도, sequntial 하게 가져오면서, 마지막 입력에 집중되는 경향이 있다. (한정된 학습 량에 마지막의 변화가 영향이 제일 클 것이므로)

각 스태이트 위치와 관계없이 중요한 데이터를 강조하여 참고할 수 있도록 하는 것이 Attention이다.  
Attention에는 3개의 값 Query, Key-Value pairs(Q,K,V)가 있다.

seq2seq model에서,  
- Q : 시간 t 에서의 디코더의 히든스테이트 (디코딩에서 현재 컨텍스트를 가지고 있는 벡터)  
- K : 시간 t 에서의 인코더의 히든스테이트**들** (대상 어텐션 대상들이 q 와 얼마나 관련이 있는지를 계산하기 위해 쓰이는 벡터 )  
- V : 시간 t 에서의 인코더의 히든스테이트**들** (실제로 값을 Weighted sum 할때 사용되는 직접적인 표현이 되는 벡터)  
(**들** 인 이유 : Q가 각각 비교하기 위해)

### Transfomer

![[34-0e3f3b4b4f.png]]

Transformer 구조

**Step 1 Input Embedding.**  
입력된 텍스트나 시퀀스 데이터를 벡터 형태로 변환하여 모델이 이해할 수 있는 숫자 형태로 만드는 과정이다. 이 과정에서는 각 단어 또는 입력 요소가 고정된 차원의 벡터로 임베딩된다.  
  
**Step 2 Positional Encoding.**  
단순히 임베딩된 벡터만으로는 순서 정보를 담기 어렵기 때문에, 각 단어의 위치 정보를 포함한 포지셔널 인코딩을 추가한다. 이는 모델이 시퀀스 내에서 단어의 순서를 인식하고, 위치에 따른 차이를 이해할 수 있게 한다.  
  
**Step 3 Multi-Head Attention.**  
여러 개의 어텐션 헤드를 사용해 입력 시퀀스의 서로 다른 부분에 집중할 수 있도록 한다. 이를 통해 모델은 문장의 다양한 맥락을 병렬적으로 학습할 수 있으며, 각 헤드는 다른 부분에 집중해 서로 다른 관점에서 정보를 추출한다.  
  
**Step 4 Add & Norm + Feed-Forward Network.**  
Add & Norm를 중간중간에 하는 이유는어텐션의 출력과 원래 입력을 더한 후, 이 결과를 정규화(Normalization)하여 학습을 안정화한다.그 후, Position-wise Feed-Forward Network를 통해 각 위치에 대해 독립적으로 선형 변환과 활성화 함수를 적용해 복잡한 패턴을 학습할 수 있도록 한다. 이 단계는 더 깊은 표현을 학습하기 위해 필수적이다.  
  
**Step 5 Decoder & Output.**  
디코더는 인코더의 출력을 받아 시퀀스를 생성하는 과정으로, 디코더에서도 Multi-Head Attention을 사용해 인코더의 출력과 디코더의 이전 출력 사이의 상호 관계를 학습한다. 마지막으로, 디코더의 최종 출력은 소프트맥스 함수를 통해 확률 분포로 변환되며, 이를 바탕으로 최종적인 출력 단어가 선택된다. 이 과정이 반복되면서 전체 시퀀스가 생성된다.
