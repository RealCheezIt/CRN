# About
# CRN (CTF Rapid Note)
**First Web Project :D**

> **Fast, Safe, and Markdown-based CTF Writeup Management System**
>  CTF 문제를 풀며 작성하는 빠른 로컬 저장 및 마크다운 기반의 오답노트 웹 애플리케이션입니다. (아직 MVP 단계)

기존 DreamHack 사이트, CTF Time 내장 ctf 랏업 기능을 써보며 불편한 점과 많은 분들이 티스토리나 노션에 많이 기록 한다는 사실을 알게 돼
단점을 보완한 웹 서비스를 만들고자 시작했습니다

---


## Tech Stack (기술 스택)

* **Backend**: Python 3, Flask
* **Database**: SQLite3
* **Frontend**: HTML5, CSS

> **사용자가 생긴다면 추후 Java, PostgreSQL로 리팩터링 예정**


## 제공 기능
* **랏업 마크다운화**
* **깃허브 푸시**
* **랏업 템플릿화**
* **태그시스템**
* **로컬 저장**
* **수정, 삭제**

## 계획 했지만 못 이룬 것들
* **모의해킹 공간 막 그런거 (드림핵에서 봄)**
* **자바스크립트를 이용한 다양한 애니메이션 유아이(자바스크립트 할 줄 모름)**
* **다크모드**



## 현재 버그
- 가입 또는 로그인에서 이름만 쓰고 엔터 치면 그냥 다음 화면 렌더링됨...
- 태그시스템 작동 안돼
- 이름 말고 비번만 치고 엔더만 쳐도 됨.... 폼 검증 필요
  
