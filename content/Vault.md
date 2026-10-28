---
tags:
  - type/moc
---

# Vault 규칙

이 볼트를 어떻게 쓸지 정해둔 문서입니다. 헷갈릴 때 여기를 봅니다. 대시보드는 [[Home]]입니다.

## 폴더 구조 (PARA)

| 폴더 | 넣는 것 | 판단 기준 |
| --- | --- | --- |
| `Project` | 끝나는 날이 있는 일 | 완료 조건을 한 문장으로 쓸 수 있는가 |
| `Area` | 계속 관리하는 영역 | 끝나지 않지만 수준을 유지해야 하는가 |
| `Resource` | 주제별 참고 자료 | 나중에 다시 찾아볼 지식인가 |
| `Archive` | 끝났거나 식은 것 | 지금 손대지 않는가 |
| `Journal` | 날짜별 기록 | 그날에만 의미 있는 내용인가 |
| `Templates` | 노트 템플릿 | 반복해서 쓰는 양식인가 |

프로젝트가 끝나면 `Project`에서 `Archive`로 옮기고, 그 안에서 다시 쓸 지식은 `Resource`로 빼냅니다.

## 파일명 규칙

- 영어로 씁니다. 본문은 한국어여도 됩니다
- 단어 첫 글자만 대문자로 씁니다. 예: `Batch Size and Learning Rate`
- 상태를 파일명에 넣지 않습니다. `(writing)` 같은 표시는 frontmatter의 `status`로 씁니다
- 약어는 그대로 대문자로 둡니다. 예: `LoRA`, `PCA`, `LLM`

## frontmatter 규칙

```yaml
---
tags:
  - type/paper
  - ai/llm
status: reading
---
```

`status`에 쓰는 값입니다.

| 값 | 의미 | 쓰는 곳 |
| --- | --- | --- |
| `draft` | 쓰다 만 노트 | 개념 노트, 팁 |
| `done` | 정리 끝난 노트 | 개념 노트 |
| `reading` | 읽는 중 | 논문 노트 |
| `read` | 다 읽음 | 논문 노트 |
| `active` | 진행 중 | 프로젝트 |
| `paused` | 멈춤 | 프로젝트 |
| `finished` | 완료 | 프로젝트 |

## 태그 규칙

폴더가 위치를 정하고, 태그는 성격을 정합니다. 폴더로 이미 표현되는 것을 태그로 또 붙이지 않습니다.

종류 태그입니다. 노트마다 하나만 붙입니다.

- `type/paper` 논문 정리
- `type/concept` 개념 노트
- `type/project` 프로젝트
- `type/daily` 데일리 노트
- `type/tip` 실무 팁, 설치법
- `type/moc` 목차 노트

주제 태그입니다. 필요한 만큼 붙입니다.

- `ai/llm`, `ai/general`, `ai/vision`
- `math`
- `dev/git`, `dev/markdown`, `dev/python`
- `life`

## 노트 쓰는 법

- 새 노트는 `Templates`에서 꺼내 씁니다
- 정리하다 만 부분은 `@@`로 표시합니다. [[Home]]에서 초안 목록으로 모입니다
- 개념 노트는 한 노트에 한 개념만 담고, 서로 위키링크로 잇습니다
- 논문 노트에서 가장 중요한 칸은 "내 코멘트"입니다. 요약만 있으면 다시 읽을 이유가 없습니다
