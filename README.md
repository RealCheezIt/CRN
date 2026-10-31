# CTF 오답노트 (CRN)
*My first web service btw👀*


CTF(Capture The Flag) 문제를 풀고 난 뒤 풀이 과정과 배운 점을 기록하는 개인용 오답노트 웹 애플리케이션입니다. Flask와 SQLite로 제작되었으며, 보안 실습을 겸한 개인 프로젝트로 시작했습니다.

## 주요 기능

- **회원가입 / 로그인** — 비밀번호는 해싱되어 저장됩니다 (`werkzeug.security`)
- **오답노트 작성/수정/삭제** — 문제 이름, 카테고리, 풀이 내용을 기록
- **태그 시스템** — 노트 하나에 여러 개의 태그를 자유롭게 붙일 수 있습니다 (다대다 관계)
- **마크다운 내보내기** — 작성한 노트를 `.md` 파일로 로컬 다운로드
- **GitHub 연동** — OAuth로 본인 GitHub 계정을 연결하고, 지정한 레포지토리에 노트를 자동 커밋
- **세션 기반 인증** — 로그인한 사용자는 본인이 작성한 노트만 조회/수정/삭제 가능

## 기술 스택

- **Backend**: Python, Flask (Application Factory + Blueprint 패턴)
- **Database**: SQLite
- **Templating**: Jinja2
- **Frontend**: HTML, CSS, Bootstrap
- **인증**: Flask 세션, GitHub OAuth

## 적용된 보안 조치

- 비밀번호 해싱 (평문 저장 금지)
- Jinja2 자동 이스케이프를 통한 XSS 방지
- CSRF 토큰 적용 (Flask-WTF)
- 세션 쿠키 보안 옵션 (`HttpOnly`, `SameSite`)
- 모든 노트 조회/수정/삭제 쿼리에 `user_id` 조건을 포함하여 타 사용자 데이터 접근 차단

## 프로젝트 구조

```
CRN/
├── app/
│   ├── __init__.py         # Flask App Factory
│   ├── config.py           # 환경변수 기반 설정
│   ├── database.py         # DB 스키마 및 쿼리 함수
│   ├── routes/
│   │   ├── auth.py         # 회원가입/로그인/GitHub OAuth
│   │   ├──__init__.py
│   │   └── notes.py        # 노트 CRUD, 내보내기, GitHub 푸시
│   ├── utils/
│   │   ├── md.py           # 마크다운 변환
│   │   └── github.py       # GitHub API 연동
│   └── templates/
├── .env                     
├── requirements.txt
└── run.py
```

## 실행 방법

1. 저장소 클론
   ```bash
   git clone https://github.com/RealCheezIt/CRN
   cd CRN
   ```

2. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```

3. `.env` 파일 생성 (프로젝트 루트에)
   ```
   SECRET_KEY=임의
   DATABASE_PATH=ctf_notes.db
   GITHUB_CLIENT_ID=깃허브_OAuth_App_ID
   GITHUB_CLIENT_SECRET=깃허브_OAuth_App_Secret
   ```

4. 서버 실행
   ```bash
   python run.py
   ```

5. 브라우저에서 `http://localhost:5000` 접속

## Feature

- 마크다운 실시간 미리보기 미구현 (내보내기/푸시 기능은 정상 작동)
- 키워드/태그 기반 검색 기능 미구현
- GitHub OAuth에 CSRF 방지용 `state` 파라미터 미적용 (추가 예정)
- 파일 첨부(스크린샷, 바이너리 등) 기능 미구현
- 장기적으로 자바(Spring) + PostgreSQL 스택으로 마이그레이션 예정

