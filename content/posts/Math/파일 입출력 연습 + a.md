---
title: "파일 입출력 연습 + a"
date: "2020-12-11"
tags: ["Math"]
aliases: ["tistory-7"]
source: "https://choimino.tistory.com/7"
---

파일 입출력 실습을 해보았는데 예전에 c언어 할때 다 했던거지만 뜨문뜨문 생각나고 잘 생각이 나지 않았는데 이렇게 실습으로 하니까 1학년때 생각 나고 공부했던거 기억나는거 같았다.

간단했지만, 파일로 나타내는거는 언제나 조금 힘든거 같다.

**#define _CRT_SECURE_NO_WARNINGS**  
**#include <stdio.h>**  
**int main()**  
**{**  
**char buffer[300];**  
**FILE* fs = fopen("embedded progrmmiprogrmming s1.txt", "r"); // 파일 포인터 선언 , 파일 읽기옵션으로.**

**FILE* resfs = fopen("embedded progrmming result.txt", "a+"); // 쓰기옵션으로 선언하기**

**while (feof(fs) == 0) {  // s1텍스트 파일 끝까지 읽고 resfs 에 쓰기**  
 **fgets(buffer, sizeof(buffer), fs);**  
**fprintf(resfs, "%s",buffer);**  
**}**

**fs = fopen("embedded progrmming s2.txt","r"); //fs를 s2로.**

**while (feof(fs) == 0) { // s2텍스트 파일 끝까지 읽고 resfs 에 쓰기**  
**fgets(buffer, sizeof(buffer), fs);**  
**fprintf(resfs, "%s", buffer);**  
**}**  
**fclose(fs);**  
**fclose(resfs);**  
**return 0;**  
**}**

![[7-939ad0c4cb.png]]

3번째 텍스트 파일이 결과파일이다.

(+a) 다하고 시간이 잠깐 남아서 현재 시간 출력하는 것도 간단하게 구현을 해보았다.

**#define _CRT_SECURE_NO_WARNINGS**  
**#include <stdio.h>**  
**#include <time.h>**  
**int main(void) {**  
**time_t t = time(NULL); // 현재시간을 가져온다**  
**struct tm tm = *localtime(&t); // 현재시간연결**  
**char* week[7] = {**  
**"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"**  
**};**  
**printf("%d/%d/%d (%s) %d:%d:%d\n",  // 출력**  
**tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, week[tm.tm_wday],**  
**tm.tm_hour, tm.tm_min, tm.tm_sec**  
**);**  
**return 0;**

**}**

![[7-0121ce5b15.png]]

생각보다 너무 간단했다..
