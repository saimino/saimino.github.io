---
tags:
  - type/tip
  - ai/llm
status: draft
---

(edit: 20231108)


##  0 : LLM을 위한 환경 초기설정

직접 구현 (우분투 22.04 LST)
 - CUDA 11.8설치
 - cudnn 11.x 최신버전 설치 (231107기준: .895)
 - conda 터미널에서 설치
 - [Pytorch](https://pytorch.org/get-started/locally/)사이트 들어가서 Getstart에서 우분투(리눅스), conda로 쿠다버전 11.8, 파이썬 선택후 터미널에서 콘다 가상환경들어간다음 커맨드 실행
 - 그 후 wandb, pandas, hugingface 같은 필요한 모듈 설치


##  1 : 하드웨어와 드라이버 

   Nvidia - CUDA (엔비디아 쓸거면 필수)

      * 가장 오랫동안 개발되고 완성도가 높다

   Apple - MPS

   AMD - ROCm

   Intel - OpenVino

   이러한 레이어의 구현체들의 공통적인 문제중 하나가 윈도우 지원이 약하다는 점이다
   CUDA 의 경우 그나마 윈도우 지원이 좀 되는 편
   애플은 어차피 자사 하드웨어용이고
   OCm 이나 OpenVino 등은 많이 뒤떨어짐
   대안으로는 WSL(윈도우용 리눅스) 을 설치하는 것이 있다
   귀찮더라도 리눅스 쓰는게 맘편함

---

      
##  2 : 기반 머신러닝 알고리즘 

pytorch (걍 이거쓰셈 LLM)

가장 많이 쓰인다. 현재 2.0.1

   [https://pytorch.org/](https://oo.pe/https://pytorch.org/ "pytorch.org/ (외부 사이트)")

   tensorflow

   예전에는 가장 많이 쓰였지만 지금은 파이토치에 밀림

   tinygrad

   해커 George Hotz가 개발한 미니멀한 딥러닝 라이브러리

   https://github.com/geohot/tinygrad

   자신의 회사가 개발하는 오픈파일럿의 구동을 위해 사용됨

   ggml

   해커 Georgi Gerganov 가 개발한 딥러닝 추론 라이브러리

   https://github.com/ggerganov/ggml

   처음에 파이토치 안 쓰고 CPU 추론하는 라이브러리로 시작했다가 CUDA, MPS 등을 지원하기 시작

   최근에 공유메모리쓰는 애플 M1 칩에서 뛰어난 가속성능을 보여줘서 관심이 다시 늘어나고 있음. 결국 이를 지켜보던 실리콘밸리의 거물 nat friedman 에게 투자받아서 회사 차림

   BLAS = Basic Linear Algebra Subprograms. 행렬 연산 등 해주는 라이브러리. 
   포트란 시절부터 존재하던 라이브러리. 
   cuBlas 는 CUDA 를 이용한 BLAS 구현체. 
   단, pytorch 의 텐서의 행렬 연산과는 서로 다르다. 
   BLAS 는 column 중심 포맷, pytorch 는 row 중심 포맷. 
   언어모델에는 별로 쓰이지 않고 있다가 ggml 라이브러리가 GPU 가속을 위한 기능으로 cuBlas 를 이용함 (pytorch 는 너무 무거워서 경량화를 추구하는 ggml 에 사용되지 않음) 생 CUDA 는 너무 low-level 이라 행렬연산등 기본 기능을 지원하는 cuBlas 를 이용한 것. 따라서 cuBlas 는 레이어 1.5 정도라고 생각할 수 있음
        
##  3 : 트랜스포머 알고리즘 + 모델 구현 (LoRA) 

   허깅페이스 트랜스포머

   https://huggingface.co/docs/transformers/index

   허깅페이스에서 개발해서 공개한 트랜스포머 라이브러리

   트랜스포머에 관련된 변종모델들이 굉장히 많은데 그것들을 다수 지원하고, 편리하게 몇줄의 코드만으로 모델을 로드하고 추론과 학습 작업을 할 수 있게 해준다

  exllama

   https://github.com/turboderp/exllama

   허깅페이스 트랜스포머의 대안으로 llama 모델에 한정해서 양자화된 모델의 추론에 최적화 시킨 라이브러리

   llama.cpp
  https://github.com/ggerganov/llama.cpp
  어떤사람이 걍 자기 맥북에서 llama 를 돌리려고 만든 프로젝트. 추론 부분은 따로 ggml 라이브러리로 떼어냈음

##  4 : 유저 인터페이스 

   실제 추론이나 학습을 위해서는 몇줄의 파이썬 코드를 짜서 돌릴 수 있지만, 코딩에 익숙하지 않은 사람에게는 이것도 진입장벽이다

   파이썬에서는 gradio 라는 라이브러리를 이용하면 쉽게 웹기반 ui 를 만들 수 있고, 이걸 이용한 소프트웨어들이 인기를 끌고 있다

   물론 gradio 를 이용하지 않은 구현체들도 있다

   AUTOMATIC1111

   가장 유명한 스테이블 디퓨전 UI

   관련된 다양한 기능들을 모두 직접 만드는 대신, 추가적인 확장기능을 다운받아서 설치할 수 있는 기능을 제공해서 일종의 생태계를 구축했다

   핵심 익스텐션으로 ControlNet 이 가장 대표적

   oobabooga (이거 써보고 싶음)

   가장 유명한 언어모델 UI
   
- ##  4-2 : API 

    유저가 직접 웹을 통해서 언어모델에 접근하는 대신, api 를 통해서 접근할 수 있게 만들어놓음

     직접 언어모델에 접근하지 않고 중간에 api 거침으로써 얻을 수 있는 이득으로는 프롬프트의 포매팅, 엠베딩의 추출과 인덱싱, 반복이나 분산을 통해 여러 단계를 거쳐야 하는 추론 요청 처리의 중개 등이 가능하다

    + LangChain
      - 가장 유명한 언어모델 활용을 위한 솔루션
      - [https://python.langchain.com/en/latest/index.html

##  (+) : 파일 포맷

 - 딥러닝 모델 파일을 저장할 때는 여러가지 선택지가 있다. 특정한 확장자가 정해진건 아니라서 혼란의 원인이 되기도 함
	1. 파이토치의 파이썬 포맷
	  - 파이토치의 자체 기능을 이용해서 저장 (모델에 포함된 각 레이어들의 정보들을 파이썬 딕셔너리 형태로 저장)  
	1. 텐서플로우의 파이썬 포맷
	   - 언어모델쪽에선 거의 안씀 걍쓰지마 

	2. 허깅페이스 포맷
	
	  - 허깅페이스는 하부 레이어로 파이토치와 텐서플로우 모두 지원하기 때문에, 이걸 이용하면 중립적인 파일포맷으로 사용 가능. 
	
	  - 허깅페이스에서 만드는 여러가지 기능들을 활용하려면 어차피 변환을 해줘야 함. 
	
	  - 초창기 LLaMA 유출본은 파이토치 포맷이었는데 사람들이 주로 허깅페이스 트랜스포머 라이브러리를 이용해서 추론을 돌리게 되자 거의 대부분 허깅페이스 변환 포맷을 주로 사용하게 됨. decapoda-research 등 허깅페이스 저장소를 통해 대부분 퍼져나감. [https://huggingface.co/decapoda-research](https://oo.pe/https://huggingface.co/decapoda-research "huggingface.co/decapoda-research (외부 사이트)")
	
	  - 메모리 상태를 쌩으로 저장하게 되면 32비트 포맷을 사용하게 되는데 허깅페이스 라이브러리에서 16비트로 저장/로드 하는 기능을 지원해줌  
	  
	1. GGML 포맷
	
	 - 허깅페이스 포맷은 주로 16 비트로 저장되는데, 메모리가 부족한 환경에서는 4비트 양자화 같은 처리가 필요함
	
	 - 양자화는 로딩타임에 바로 할 수 있는 것 (RTN = Round To Nearest) 은 8bit 까지가 한계고 4비트부터는 먼저 데이타를 쭉 읽어서 데이타의 분포와 적절한 그룹사이즈를 정해야 성능 손실을 최소화할 수 있음
	
	 - 따라서 모델 변환에는 컴퓨팅파워가 많이 필요한데, TheBloke 라는 레딧 유저가 새로운 모델이 나올때마다 거의 자선봉사하다시피 몇시간만에 뚝딱뚝딱 양자화된 결과물을 올려주고 있어 많은 유저들의 감사를 받고 있음.
	
	 - ggml 은 효율적이긴 하지만 소수의 개발자가 빠르게 개발하다보니 계속 파일포맷이 바뀌고 있음

	1. GPTQ 포맷
	
	 - GGML 과는 별도로 웨이트를 양자화시킨 포맷
	
	 - GPTQ 라는 논문 ([https://arxiv.org/abs/2210.17323](https://oo.pe/https://arxiv.org/abs/2210.17323 "arxiv.org/abs/2210.17323 (외부 사이트)")) 을 기반으로 파이썬 구현체 ([https://github.com/IST-DASLab/gptq](https://oo.pe/https://github.com/IST-DASLab/gptq "github.com/IST-DASLab/gptq (외부 사이트)")) 가 나왔으며, 그걸 우리 챈러 qwopqwop 이 LLaMA 용으로 포팅 ([https://github.com/qwopqwop200/GPTQ-for-LLaMa](https://oo.pe/https://github.com/qwopqwop200/GPTQ-for-LLaMa "github.com/qwopqwop200/GPTQ-for-LLaMa (외부 사이트)"))
	
	 - 초반에는 GPU 용 양자화는 GPTQ, CPU 용 양자화는 GGML 같은 느낌이었는데, GGML 이 GPU 도 지원하기 시작하면서 구분이 모호해짐.
	
	 - 양자화된 파일은, 그룹사이즈, 비트수의 배분 등 여러가지 바리에이션이 있기 때문에 우바부가 기준으로 파일명에 규칙을 정해서 관리하는 편임

	1. ONNX 포맷
	
	 - 서로 다른 딥러닝 프레임워크 (파이토치, 텐서플로우) 간의 표준적인 모델 교환을 위해 만들어진 포맷
	
	 - 하지만 비슷한 역할을 허깅페이스 트랜스포머가 하다보니 언어모델에서는 큰 관심은 받지 못함. 디퓨전쪽에서는 nvidia 이외의 환경에서 모델을 돌리기 위해서 쓰는 경우가 있었던 것 같음



