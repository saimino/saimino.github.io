---
title: "리눅스에서 쿠다(CUDA) 버전 확인하는 법"
date: "2024-07-20"
tags: ["AI"]
aliases: ["tistory-32"]
source: "https://choimino.tistory.com/32"
---

```bash
python -c "import torch; print(torch.version.cuda)"
```

리눅스 CLI에서 바로 실행하면 나온다
