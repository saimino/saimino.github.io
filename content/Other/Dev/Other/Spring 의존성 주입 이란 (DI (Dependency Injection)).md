---
title: "[Spring] 의존성 주입 이란 (DI (Dependency Injection))"
date: "2023-05-13"
tags: ["Others", "Web"]
aliases: ["tistory-25"]
source: "https://choimino.tistory.com/25"
---

의존성 주입 : 단어만 들으면 동사의 느낌이라서 의존성을 주는 '상태'가 떠올려지는데, 아니다.  
어떤 객체에서 다른 객체를 사용할 때 직접 만들어서 사용하는 것이 아니라, setter, 생성자 등 을 사용해서 주입하는 '방법' 이다.

![[25-b7f2fa28c7.png]]

출처 : https://m.blog.naver.com/PostView.nhn?blogId=ljh0326s&logNo=221395815870&proxyReferer=https:%2F%2Fwww.google.com%2F

장난감은 배터리에 의존하고 있는데, (장난감은 베터리 상황에 영향을 받는다는 뜻)  
배터리 일체형은 만들어 질때 베터리가 함께(내부에서 의존성을 주입) 나오고 있고  
배터리 분리형은 베터리가 소모(변경)하면 교체가능(외부에서 의존성 주입) 하다.

![[25-3a854f805e.png]]

출처 : https://m.blog .naver.com/PostView.nhn?blogId=ljh0326s&logNo=221395815870&proxyReferer=https:%2F%2Fwww.google.com%2F

코드로 보면,  
배터리 일체형은 생성자에서만 의존성을 주입하고 있어서 베터리 교체가 불가능하다.
