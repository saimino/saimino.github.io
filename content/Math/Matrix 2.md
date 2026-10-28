---
tags:
  - type/concept
  - math
status: draft
---

Rank @@@
- 어떤 행렬에서 어떤 벡터가 독립이고, 다른 공간을 만들 수 있는 벡터의 개수
- 각 벡터를 사칙연산을 해서 벡터를 만들 수 있으면 Rank 에서 해당 열을 제외해서 가지는 행렬
- 또한, rank(A)=rank(A^T) 를 만족한다.
Full Rank @@@
- 어떤 행렬의 행과 열의 크기 중 작은 값과 Rank가 같다면, Full Rank임
- 직사각형의 행렬에서는 행과 열중 작은 값이 Rank의 최댓값이다.
- 또한, rank(A) 는 항상 min(m,n)보다 작거나 같다.

Linear Equation @@@
- m이 row(수식, 점) n이 colunms (미지수) 라고 할 때, 
- m = n 이면 하나의 해가 나온다
- m > n 이면 (즉, 미지수가 작으면) 해가 정확하게 안나온다. - > 근사화를 해야함
- m < n 이면 (즉, 수식이 작으면) 해가 무한으로 나온다. - > 제약조건 필요

Column Space @@@
- 행렬 A의 Column vector 들로 만들 수 있는 부분 공간 span(V1, V2, ... Vn) 
- Ax = b 가 존재 하려면 b가 행렬 A의 컬럼스페이스에 있어야함.

Null Space
- Ax = 0를 만족하는 x의 집합
- x=x' + (A의 Null Space)  

Least Squares method (최소자승법) (https://m.blog.naver.com/PostView.naver?blogId=skkong89&logNo=221430620894&categoryNo=47&proxyReferer=) @@@
- Ax = b 를 approximation 하는 것
- 투영(projection)해서 찾는 것
- 즉, Ax' = p 를 찾아야 한다. (p는 b직선이 approximation 된 것이므로 결국 x'을 찾으면 p를 구할 수 있다.)
- x' = (A^T A)^-1 A^T b @@@ 식 외워야함

Eigenvalue and Eigenvector @@
- 정방행렬 A에 대하여 Ax = λx  (상수 λ) 가 성립하는 0이 아닌 벡터 x가 존재할 때 상수 λ 를 행렬 A의 고유값 (eigenvalue), x 를 이에 대응하는 고유벡터 (eigenvector) 라고 한다.
- Eigenvalue 와 Eigenvector 는 정방행렬의 디멘젼만큼 갯수가 존재한다.
- Eigenvector(고유벡터)
	- 0이 아닌 어떤 벡터에 Eigenvector 를 곱 했을때, 방향은 변하지 않고 크기만 변하는 벡터
- Eigenvalue 
	 - 대응되는 고유벡터의 변화되는 스케일의 정도

- Covariance(공분산)
	- 분산: 평균을 구하고, 해당 변수의 평균을 뺀 편차를 구하고, 제곱해서 다더하고 n(데이터의 개수)으로 나눠준다.
	- 공분산 : 제곱을 하는대신 해당 편차를 곱해주고 시그마한다. n으로 나눠준다.
	- 공분산은 확률변수의 상관정도를 나타낸다. 
	- X와 Y가 독립이라면, 두 변수에대한 공분산은 0이다.
- Covariance Matrix (공분산 행렬) @@@ (다시 듣기)
	- M개의 다변수 확률변수 벡터가 존재할때
	- 대각성분은 해당 변수만의 공분산. 나머지는 대각행렬에 해당하는 변수 두개의 공분산을 정의한다.


+해가 존재하고 유일하려면 행렬 랭크가 변수의 개수와 동일해야함.