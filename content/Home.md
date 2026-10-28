---
tags:
  - type/moc
---

# Home

볼트 전체를 한눈에 보는 대시보드입니다. 규칙은 [[Vault]]에 정리해뒀습니다.

## 진행 중 프로젝트

```dataview
TABLE status AS "상태", deadline AS "마감"
FROM "Project"
WHERE status != null
SORT deadline ASC
```

## 열린 할 일

```dataview
TASK
FROM "Project" OR "Journal"
WHERE !completed
GROUP BY file.link
```

## 읽는 중인 논문

```dataview
TABLE status AS "상태", year AS "연도", venue AS "학회"
FROM "Resource/AI/Paper"
SORT file.mtime DESC
```

## 마무리 안 된 초안

```dataview
LIST
FROM -"Templates"
WHERE status = "draft"
SORT file.mtime DESC
```

## 내용이 비어 있는 노트

```dataview
LIST
FROM -"Templates"
WHERE file.size < 100
SORT file.folder ASC
```

## 최근에 손댄 노트

```dataview
TABLE dateformat(file.mtime, "yyyy-MM-dd") AS "수정일", file.folder AS "위치"
FROM -"Templates" AND -"Journal"
SORT file.mtime DESC
LIMIT 10
```

## 바로가기

- [[Vault]] 볼트 규칙
- [[LLM]] LLM 아키텍처
- [[Tips]] 잡다한 팁

## 주제별 노트

```dataview
TABLE rows.file.link AS "노트"
FROM -"Templates" AND -"Journal"
GROUP BY file.folder AS "폴더"
SORT key ASC
```
