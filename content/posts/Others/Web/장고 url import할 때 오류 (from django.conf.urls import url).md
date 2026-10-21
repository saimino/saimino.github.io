---
title: "장고 url import할 때 오류 (from django.conf.urls import url)"
date: "2023-03-03"
tags: ["Others", "Web"]
aliases: ["tistory-20"]
source: "https://choimino.tistory.com/20"
---

![[20-7c74df7f17.png]]

django4.0 부터 없어진 함수 그대로 사용하려면

```capnproto
from django.urls import re_path as url
```

을 사용해야한다.

+) 없어진 url함수 말고 다른 함수를 싶다면,

```gradle
from django.urls import include, re_path
```

아니면 url 함수를 re_path 함수로 변경하면된다. 둘다 정규식을 사용하기 때문에 함수의 매개변수는 변경하지 않아도 된다.
