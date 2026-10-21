---
title: "단정도 숫자의 이진표현 출력 (S/E/F)"
date: "2020-12-11"
tags: ["Math"]
aliases: ["tistory-5"]
source: "https://choimino.tistory.com/5"
---

ieee 754 단정도 숫자 출력 실습을 해보았다.

그렇게 힘들지는 않았지만, 이것이 존재한다고만 생각했었지 실제로 출력해볼 생각을 하지 않아서 코드 작성할 때 약간 고민했다. 배운게 그대로 사용되고 있다고 하는게 당연하지만 신기했다.

낮은 레벨 축에도 못끼지만 낮은레벨 공부하는 것도 충분히 재미있는거 같다.

**#include <stdio.h>**  
**typedef**  
**union{**  
**float x;**  
**struct{  //  IEEE 754 단정도 숫자를 출력하기 위한 범위 자르는 구조체**  
**unsigned f:23;**  
**unsigned e:8;**  
**unsigned s:1;**  
**} p;**  
**} print_fp_ value;**

**int main()**  
**{**  
**print_fp_value num;**  
**printf("Single precision FP value: ");**  
**scanf("%f",&num.x);**

**printf(" nS: %d",num.p.s); // 부호**

**printf(" nE: "); // 지수**  
**for(int i=7;i>=0; i)**  
**printf("%d",(num.p.e>>i)&1);**

**printf(" nF: "); // 가수**  
**for(int i=22;i>=0; i)**  
**printf("%d",(num.p.f>>i)&1);**  
**}**

![[5-b18f3915e0.png]]

구름 ide에서 출력해본 모습
