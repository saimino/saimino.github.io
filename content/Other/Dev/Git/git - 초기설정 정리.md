---
title: "git - 초기설정 정리"
date: "2023-08-23"
tags: ["Others", "Others"]
aliases: ["tistory-28"]
source: "https://choimino.tistory.com/28"
---

git을 설치하기 위해서는 git bash의 설치가 필요하다.

git 설치는 아래의 링크를 참고해 설치한다.

<https://code-lab1.tistory.com/249>

> [(Git) 윈도우10(window 10) 깃(Git) 설치하기 - Git 기초(0.5)](https://code-lab1.tistory.com/249)  
> code-lab1.tistory.com

그 후,

github웹에서 repo초대받았다면, clone을 해야한다.  
(clone은 이미 레포지토리가 만들어져 있고, 내가 만들었거나 초대되어 있다면 clone이 되고 자동으로 내 로컬과 원격저장소가 연결이 된다.)  
  
git clone {저장소 URL}  
특정 브랜치만 clone 하고 싶다면  
git clone -b {브랜치이름} --single-branch {저장소 URL}

하면 설정은 끝이다.
