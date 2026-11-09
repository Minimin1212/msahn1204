# msahn1204

이 저장소는 [Academic Research Skills (ARS)](https://github.com/Imbad0202/academic-research-skills) 플러그인을 사용하도록 설정되어 있습니다.
`.claude/settings.json`에 플러그인이 등록되어 있어서, 이 폴더에서 Claude Code를 열면 플러그인 설치를 묻고 자동으로 활성화됩니다.

## 사용법

자연어로 원하는 작업을 말하면 Claude가 알맞은 스킬과 모드를 고릅니다.

| 하고 싶은 일 | 이렇게 말하거나 입력 |
|---|---|
| 막연한 아이디어로 연구 질문 다듬기 | "○○에 관심이 있는데 연구 질문을 같이 잡아줘" |
| 빠른 문헌 요약 | "○○ 관련 문헌을 빠르게 정리해줘" |
| 체계적 문헌고찰 (PRISMA) | "○○에 대해 체계적 문헌고찰을 해줘" |
| 논문 구조 계획 (소크라테스식 대화) | `/ars-plan` |
| 개요 + 근거 지도 | `/ars-outline` |
| 문헌고찰 형식의 주석 참고문헌 | `/ars-lit-review` |
| 초록 + 키워드 (이중 언어) | `/ars-abstract` |
| 인용 오류 점검 | `/ars-citation-check` |
| 모의 동료 심사 | `/ars-reviewer` |
| 심사 의견 반영 수정본 + 답변서 | `/ars-revision` |
| 수정 로드맵 코칭 | `/ars-revision-coach` |
| LaTeX / DOCX / PDF / Markdown 변환 | `/ars-format-convert` |
| 연구 → 집필 → 심사 → 수정 → 완성 전체 파이프라인 | `/ars-full` |

전체 파이프라인은 단계마다 멈추고 사용자의 확인을 받습니다.

## 논문용 그림 만들기 (scientific-figure-making 스킬)

`.claude/skills/scientific-figure-making/`에 [figures4papers](https://github.com/ChenLiu-1996/figures4papers)의 그림 스킬이 들어 있습니다.
matplotlib로 학술지 수준의 막대그래프, 추세선, 히트맵, 레이더 차트, 여러 패널 그림을 만들어 줍니다.

예시 요청:
- "이 데이터로 모델 성능 비교 막대그래프를 논문용으로 그려줘. PNG와 PDF로 저장해줘"
- "월별 추이를 논문용 선 그래프로 그려줘"

## 영상·팟캐스트 요약 (playback-notes 스킬)

`.claude/skills/playback-notes/`에 [playback-notes](https://github.com/AgwaB/playback-notes)가 들어 있습니다.
강의, 학회 발표, 팟캐스트를 요약 보고서(HTML, Markdown, PDF)로 만들고, 모든 내용에 녹화의 시간 표시를 달아 줍니다.
세션이 시작될 때 `.claude/hooks/session-start.sh`가 Node.js 24와 필요한 패키지를 자동으로 설치합니다.

예시 요청:
- "첨부한 강의 자막 파일로 핵심 요약 보고서 만들어줘" (SRT, VTT, TXT)
- "첨부한 발표 영상 깊이 있게 분석해서 PDF로 줘"

유튜브, X, Apple Podcasts 링크를 쓰려면 클라우드 환경 설정의 네트워크 허용 도메인에
`www.youtube.com` 등을 추가해야 합니다.

## 데이터 분석과 글쓰기 보조 (knowledge-work-plugins에서 고른 스킬)

[anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)에서 외부 서비스 연결이 필요 없는 스킬 5개만 `.claude/skills/`에 넣었습니다.

- `explore-data`: 데이터 파일의 구조, 결측치, 이상값을 먼저 훑어봅니다.
- `statistical-analysis`: 기술통계, 가설검정, 이상치 탐지 방법을 알려 줍니다 (자동으로 참고).
- `validate-data`: 분석을 공유하거나 투고하기 전에 방법과 편향, 계산 오류를 점검합니다.
- `draft-content`: 뉴스레터, 블로그, SNS 글의 초안과 제목 후보를 만듭니다.
- `content-creation`: 위 초안 작성의 채널별 형식 가이드입니다 (자동으로 참고).

## 계획 점검 (/grill-me)

[mattpocock/skills](https://github.com/mattpocock/skills)의 `grill-me`와 `grilling` 스킬이 `.claude/skills/`에 들어 있습니다.
`/grill-me`를 입력하고 점검받고 싶은 계획을 말하면, Claude가 의사결정 가지를 하나씩 따라가며 집요하게 질문합니다. 질문마다 Claude의 추천 답이 붙어 있어서 맞으면 "네"라고만 답해도 됩니다.
모든 가지를 살펴볼 때까지 계속되고, 합의했다고 확인하기 전에는 실행하지 않습니다.

예시: `/grill-me 내 논문의 연구 설계`, `/grill-me 뉴스레터 월간 발행 계획`

## 문체 다듬기 (/humanizer)

[blader/humanizer](https://github.com/blader/humanizer)의 스킬이 `.claude/skills/humanizer/`에 들어 있습니다.
AI가 쓴 티가 나는 글(`~가 아니라 ~이다` 식의 대비, 한 줄짜리 마무리 문장, 억지로 맞춘 3개 나열, 부풀린 표현 등)을 찾아서, 내용은 그대로 두고 글쓴이의 말투로 고쳐 줍니다.
문체 편집 도구이고, AI 탐지기를 피하는 것은 목표가 아닙니다. 논문에 AI를 썼다면 투고처 규정에 따라 `/ars-disclosure`로 공개 문구를 만드세요.

예시: `/humanizer` 다음에 글을 붙여넣기, 내 예전 글을 함께 주면 그 말투에 맞춰 줍니다.
영어 글에 가장 잘 맞고, 한국어는 같은 종류의 패턴만 비슷하게 잡아냅니다.

## 한국어 글 윤문 (/humanize-korean)

[nathankim0/humanize-korean](https://github.com/nathankim0/humanize-korean)의 스킬이 `.claude/skills/humanize-korean/`에 들어 있습니다.
한국어 글의 사실과 의미는 그대로 두고 AI 티, 번역투, 맞춤법, 군더더기, 경어법을 다듬습니다. 모드는 AI 티 제거, 전체 윤문, 교정·교열, 문장 다듬기, 번역 윤문, 문체 변환, AI 신호 진단, 공동 교정의 8가지입니다.
AI 탐지기 회피가 목표가 아니며, 가짜 경험이나 수치, 일부러 낸 오탈자로 사람 글처럼 위장하지 않습니다.
긴 글은 문장 단위 작업표로 나눠 빠짐없이 처리하며, 이 과정에는 Python 3이 필요합니다.

예시: `/humanize-korean` 다음에 글을 붙여넣기, "보수적으로 맞춤법만 봐줘", "존댓말로 바꿔줘"
영어 글은 `/humanizer`, 한국어 글은 `/humanize-korean`을 쓰세요.

## 참고

- 라이선스: ARS와 scientific-figure-making은 CC BY-NC 4.0 (비상업적 이용만 가능), playback-notes는 MIT, knowledge-work-plugins 스킬은 Apache 2.0, grill-me, humanizer, humanize-korean은 MIT
- 한국어 문서: https://github.com/Imbad0202/academic-research-skills/blob/main/README.ko-KR.md
