---
title: "리엑트 (장고) proxy설정 오류"
date: "2023-03-08"
tags: ["Others", "Web"]
aliases: ["tistory-21"]
source: "https://choimino.tistory.com/21"
---

원래는 package.json에서 프록시 설정을 해주어야 했는데, 병렬로 하려고 하면 오류뜸

```1c
"proxy": {
  "/api": {
    "http//localhost:8000"
  }
}
```

/src/setProxy.js 를 만들어서 아래와 같은 코드를 써준다. (별도의 import없이 setProxy.js만들면 감지됨)

```coffeescript
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = (app) => {
   app.use(
      createProxyMiddleware('/api', {
         target: 'http://localhost:8000',
         changeOrigin: true,
      })
   );
};
```
