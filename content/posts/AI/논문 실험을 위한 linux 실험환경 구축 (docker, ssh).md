---
title: "논문 실험을 위한 linux 실험환경 구축 (docker, ssh)"
date: "2025-02-05"
tags: ["AI"]
aliases: ["tistory-41"]
source: "https://choimino.tistory.com/41"
---

## 1. Introduction

새로운 실험을 할때마다, 도커를 새로 만들고 또 찾아보고 계속 반복되는게 귀찮아서,  
경험상 딥러닝 실험 환경을 구축하고 관리하기 가장 좋은 방법을 기록하고자 한다.  
  
내 딥러닝 실험환경의 구조는,  
서버ssh(도커1ssh, 도커2ssh,...) 이렇게 이루어진다.

도커는 콘다같이 가상환경처럼 사용할 수 있다.  
(하지만 근본적으로 다르긴하다. 도커는 운영체제 수준의 가상화다.)

## 2. Method

### 1 Server 에서의 환경 구축(서버 ssh)

서버 환경은 다음과 같다.

- ubuntu 22.04
- docker 24.0.7

#### (1) SSH 설치

```bash
apt-get update  
apt-get install nano net-tools openssh-server
```

필요한 것들을 설치해준다음, 서버에서 어떤 포트를 사용할지 지정해줘야한다.

```bash
nano /etc/ssh/sshd_config
```

nano 는 파일내용을 편집할 수 있는 툴이다. nano를 사용하여 sshd_config 파일의 중간에  Port, PermitRootLogin의 앞의 #을 지우고 아래와 같이 수정한다.

![[41-f52abf0064.png]]

서버의 포트를 열어준다. 22번 포트가 기본이다. (포트는 다른 ssh나 포트를 쓰는 프로그램과 겹치지 않아야함)

![[41-7f938562ea.png]]

Ctrl+X, Y를 눌러 내용을 저장한다.

passwd root를 사용하여 비밀번호를 입력, 재입력하여 설정한다.

```sh
service ssh start
```

이제, 서버 외부에서 작업 할 수 있다.  
이제부터는 서버에서 하지않고, 로컬에서 쭉 진행한다.

#### +)접속테스트

맥 터미널이나, putty, iterm, tuminus같은 ssh bash 툴을 사용해도 된다.  
맥 기본앱인 Terminal을 예시로 들면,

![[41-9f46a06a35.png]]

터미널 메뉴바

Shell -> New Remote Cobbection... -> 오른쪽 하단 +버튼 -> connect 눌러 위의 패스워드를 입력하면,

![[41-b3771c1255.png]]

터미널에서 서버의 ssh접속

이렇게 외부에서 서버를 사용할 수 있다.

#### (2)Docker 환경 구축

sudo apt-get install ./docker-desktop-amd64.deb  
docker -v # 설치한 도커 버전 확인

![[41-aaf68df6ef.png]]

####

#### A. Container 띄우기

![[41-22e48f3f5d.png]]

```dockerfile
FROM huggingface/transformers-pytorch-deepspeed-latest-gpu

WORKDIR /workspace/midilm
```

(Dockerfile) PyTorch 이미지

```bash
#!/bin/bash

docker build -t Env .

docker run -it --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 --name general -v /root/data:/workspace/mtmoe Env bash
```

(run_docker.sh)

#### 각 옵션 설명:

-it  
→ 터미널과 상호작용 가능하도록 설정 (interactive + tty)

--gpus all  
→ **모든 GPU**를 Docker 컨테이너에 사용하게 함 (NVIDIA GPU 환경일 때 사용)

--ipc=host  
→ **공유 메모리 영역을 호스트와 공유**하게 함 (PyTorch처럼 공유 메모리 많이 쓰는 앱에 필요)

--ulimit memlock=-1  
→ 메모리를 무제한으로 lock 할 수 있게 설정 (메모리 관련 제한 해제)

--ulimit stack=67108864  
→ 스택 크기를 64MB로 설정 (기본값보다 크게 설정)

--name general  
→ 컨테이너 이름을 general로 지정

-v /root/data:/workspace/mtmoe  
→ 컨테이너 안에서 /workspace/mtmoe로 접근하면 실제로는 호스트의 /root/data를 보게 함 (공유)  
→ 호스트의 /root/data 디렉토리를 컨테이너의 /workspace/mtmoe 디렉토리에 **마운트한다** 라고 함

Env  
→ 실행할 Docker 이미지 이름 (위에서 만든 Env 이미지)

bash  
→ 컨테이너 실행 후 바로 bash 쉘을 실행  
  
+ 이미 만들어진 컨테이너 옵션 확인 방법:

docker inspect (컨테이너이름또는ID)

#### B. Container에서 ssh 열기

Docker 컨테이너를 완전히 격리된 서버처럼 쓰고 싶다면, 컨테이너 내부에서 SSH 서버를 띄워서

**Docker 내부에도 SSH로 접속**할 수 있게 만들 수 있다.

컨테이너 내부에서, 1. (1)ssh 설치를 다시진행하면 된다.

주의할 점은, **ssh를 열때, 베이스와 포트가 겹치치 않아야 한다!**

### 2 Local 에서의 환경 구축(맥북)

파이참에서:

로컬의 경로는 자동으로 잡혀있을것이다. 문제는 서버에서의 경로를 잡아야되는데, 보통 workspace로 잡는다. 그럼 로컬 프로젝트에 있는 파일이 자동으로 workspace폴더에 넣어질 것이다.

![[41-59cf361ff6.png]]
