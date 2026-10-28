---
title: "데이터베이스  - SQL"
date: "2023-04-26"
tags: ["Others", "Database & OS"]
aliases: ["tistory-24"]
source: "https://choimino.tistory.com/24"
---

![[24-a58f8f8250.png]]

설명 하면서 필요한 테이블들

- 1. SQL

SQL 기능에 따른 분류

- 데이터 정의어 (DDL)
  - 테이블이나 관계의 구조를 생성하는 데 사용
  - CREATE, ALTER, DROP 문 등이 있음

- 데이터 조작어 (DML)
  - 테이블에 데이터를 검색, 삽입, 수정, 삭제하는데 사용
  - SELECT, INSERT, DELETE, UPDATE문 등이 있음
  - SELECT문은 질의어(query, 쿼리) 라고 함

- 데이터 제어어 (DCL)
  - 데이터의 사용 권한을 관리하는 데 사용
  - GRANT, REVOKE 문 등이 있음

2. 데이터 조작어

![[24-e65838d9e2.png]]

SQL검색 문법

SQL문 내부적 실행순서 : FROM(테이블이름)-> WHERE(조건으로 필터링) -> SELECT(해당속성만 출력)

SELECT 문의 기본 문법

SELECT 속성 (AS 별칭)  
(FROM) 테이블 이름 (AS 별칭)  
(WHERE) 검색 조건  
(HAVING) 검색 조건  
(UNION (ALL))  
(ORDER BY) 속성이름

- SELECT, FROM 절

속성의 입력순서는 상관없음.

모든 속성을 선택하고 싶을 땐, * 입력  
(SELECT *)

튜플의 중복을 제거 하고 싶으면 DISTINCT 키워드를 사용  
SELECT DISTNCT  속성

- WHERE 절

![[24-d94d028805.png]]

WHERE절에 조건으로 사용할 수 있는 술어

비교  
WHERE 속성 < 20000;

범위  
WHERE price BETWEEN 10000 AND 20000  
WHERE price >= 10000 AND price <= 20000  
두 개 다 같은 출력이 나옴

NULL  
NULL을 검색할때는 비교연산자를 사용하지 말고 IS (NOT) NULL 연산자를 사용해야함

집합  
WHERE (NOT) IN ('굿스포츠','대한미디어')  
WHERE (NOT) (publisher ='굿스포츠' OR publisher = '대한미디어')  
두 개 다 같은 출력이 나옴

패턴  
WHERE bookname LIKE '축구의 역사';  
WHERE bookname LIKE '%축구%';  
WHERE bookname LIKE '_구%'

![[24-944875f7d6.png]]

와일드 문자의 종류

복합조건  
WHERE LIKE '%축구%' AND price >=20000  
WHERE publisher='굿스포츠' OR publisher='대한미디어'

- ORDER BY 절

ORDER BY price DESC, publisher ASC  
=> DESC : 내림차순, ASC : 오름차순

- 집계함수

SUM(),AVG(),COUNT(),MAX(),MIN()

- GROUP BY절

GROUP BY custid

HAVING count(*) >= 2

![[24-6132bbdcbb.png]]
