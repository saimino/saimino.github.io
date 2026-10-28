---
title: "리눅스 쿠다(CUDA) 버전 확인하는 법"
date: "2021-07-25"
tags: ["AI"]
aliases: ["tistory-15"]
source: "https://choimino.tistory.com/15"
---

```bash
python -c "import torch; print(torch.version.cuda)"
```

리눅스 CLI에서 바로 실행하면 나온다
