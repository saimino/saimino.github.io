---
title: "AI연구 오류 정리"
date: "2025-04-17"
tags: ["AI"]
aliases: ["tistory-42"]
source: "https://choimino.tistory.com/42"
---

(2025.04.17 업데이트)

### 1. ModuleNotFoundError: No module named 'torch.nn.attention'

```bash
ModuleNotFoundError: No module named 'torch.nn.attention'
```

torch.nn.attention은 **PyTorch 2.1 이상**에서 도입된 새로운 attention 관련 모듈 / PyTorch 업데이트 해야함

-> 해결법

```bash
pip install --upgrade torch --extra-index-url https://download.pytorch.org/whl/cu121
```

118은 쿠다버전임 ([[리눅스 쿠다(CUDA) 버전 확인하는 법|쿠다버전확인하는법]])

### 2. RuntimeError: Attempting to deserialize object on CUDA device 3 but torch.cuda.device_count() is 3

```bash
RuntimeError: Attempting to deserialize object on CUDA device 3 but torch.cuda.device_count() is 3
```

PyTorch에서 모델을 .pt 또는 .bin으로 저장할 때, 내부적으로 **“이 텐서는 어떤 GPU에서 저장되었는가”** 정보를 같이 저장하기 때문에

예를 들어, 저장 당시 GPU 3 (cuda:3)에서 모델이 있었다면,

다시 불러올 때도 **그 위치로 로딩하려고 함**. 예전에 학습할때는 3090 * 4였는데, 지금은 4090 * 3 이기 때문에,

cuda:3(0,1,2만 존재)는 존재하지 않음 → 그래서 에러남. 모델을 불러올때, 자동으로 매핑하게 하려면,

```bash
torch.load("model.pt", map_location="cuda")  # 자동으로 현재 GPU 중 하나에 매핑
```

(pt파일과 bin파일 모델은 텐서 정보, 기울기 등등 다 저장함)
