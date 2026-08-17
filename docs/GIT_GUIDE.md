# 🌿 Git 사용법 (daily_news_digest)

> Git이 처음이어도 괜찮습니다. 위에서부터 그대로 따라 하세요.

---

## 목차

1. [핵심 용어 3개](#1-핵심-용어-3개)
2. [최초 1회 세팅](#2-최초-1회-세팅)
3. [매일 작업하는 흐름 ⭐](#3-매일-작업하는-흐름-)
4. [Pull Request 올리기](#4-pull-request-올리기)
5. [충돌(conflict) 해결](#5-충돌conflict-해결)
6. [자주 하는 실수 되돌리기](#6-자주-하는-실수-되돌리기)
7. [절대 하면 안 되는 것 🚫](#7-절대-하면-안-되는-것-)
8. [치트시트](#8-치트시트)

---

## 1. 핵심 용어 3개

| 용어 | 뜻 |
|------|-----|
| `commit` | 변경사항을 한 묶음으로 "저장" |
| `push` | 내 커밋을 GitHub로 "올리기" |
| `pull` | GitHub의 최신 코드를 내 PC로 "받아오기" |

브랜치는 3종류만 있습니다: `main`(배포 가능 상태) · `dev`(팀 통합) · `hoya`/`whiteclover`(각자 작업).
**작업은 항상 내 이름 브랜치에서만** 합니다.

---

## 2. 최초 1회 세팅

```bash
git config --global user.name "본인이름"
git config --global user.email "github가입이메일@example.com"   # ⚠️ GitHub 계정 이메일과 동일해야 함
git config --global core.autocrlf true                          # 줄바꿈 문제 방지 (Windows 권장)
```

```bash
git clone https://github.com/whiteclover0542/daily_news_digest.git
cd daily_news_digest
```

---

## 3. 매일 작업하는 흐름 ⭐

```bash
# (1) 내 브랜치로 이동, dev 최신 내용 받아오기 — 작업 시작 전 항상!
git checkout hoya
git merge dev

# (2) 코드 작업... 그리고 저장(커밋)
git status                              # 뭐가 바뀌었는지 먼저 확인
git add .
git commit -m "feat: 뉴스 수집기 초안 추가"

# (3) GitHub로 올리기
git push

# (4) 기능 하나 끝나면 GitHub에서 Pull Request 생성 (4번 참고)
```

> 커밋은 자주, 작게. 메시지는 `feat:`(기능) · `fix:`(버그수정) · `docs:`(문서) 처럼 앞에 종류를 붙입니다.

---

## 4. Pull Request 올리기

1. `git push` 후 터미널에 뜨는 PR 링크 클릭 (또는 GitHub 레포 → "Compare & pull request")
2. **base: `dev`** ← **compare: 내 브랜치** 인지 확인 ⚠️ (base가 main이면 안 됨)
3. 제목/설명 간단히 작성 후 **Create pull request**
4. 상대방(hoya ↔ whiteclover)에게 리뷰 요청 → 확인되면 **Merge**
5. 머지된 뒤에도 내 브랜치는 지우지 않고 계속 사용 → 다음 작업 전 `git merge dev`로 최신화

> `main`은 배포 가능한 상태만 올라갑니다. `dev → main`은 둘이 상의 후 진행합니다.

---

## 5. 충돌(conflict) 해결

같은 파일의 같은 줄을 서로 고치면 충돌이 납니다. **당황하지 않아도 됩니다.**

```
<<<<<<< HEAD
내 코드
=======
가져오는 코드
>>>>>>> dev
```

1. `<<<<<<<` / `=======` / `>>>>>>>` 표시를 지우고, 남길 코드만 정리
2. 저장 후:
   ```bash
   git add <충돌났던파일>
   git commit
   ```
3. 헷갈리면 상대방에게 바로 물어보기 (VS Code의 "Accept Current/Incoming" 버튼 써도 됩니다)

---

## 6. 자주 하는 실수 되돌리기

| 상황 | 해결 |
|------|------|
| 커밋 메시지 오타 (아직 push 전) | `git commit --amend -m "올바른 메시지"` |
| `add` 잘못함 (커밋 전) | `git restore --staged <파일>` |
| 파일 수정 통째로 되돌리기 (커밋 전) | `git restore <파일>` ⚠️ 변경 사라짐 |
| 방금 커밋 취소 (변경은 유지) | `git reset --soft HEAD~1` |
| `.env`를 실수로 커밋함 | 즉시 알리고 `git rm --cached .env` 후 다시 커밋 |

---

## 7. 절대 하면 안 되는 것 🚫

1. ❌ `main`·`dev`에 직접 push → 항상 내 브랜치 + PR
2. ❌ `.env` / API 키 커밋 → `.gitignore` 확인
3. ❌ `git push -f` (강제 푸시) — 정말 필요하면 먼저 상의
4. ❌ 상대방 브랜치를 마음대로 머지/삭제

---

## 8. 치트시트

```bash
# 매일 작업 시작 — 내 브랜치 + dev 최신 반영
git checkout 내이름
git merge dev

# 저장 & 올리기
git status
git add .
git commit -m "feat: 한 줄 설명"
git push

# 현재 상태 확인용
git status
git log --oneline
git branch
```
