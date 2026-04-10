# Windows 에서 pgvector 설치 가이드

## 현재 제공된 명령어의 문제점

```batch
set "PGROOT=C:\Program Files\PostgreSQL\18"
cd %TEMP%
git clone --branch v0.8.2 https://github.com/pgvector/pgvector.git
cd pgvector
nmake /F Makefile.win
nmake /F Makefile.win install
```

### 필요한 것들

1. **Visual Studio Build Tools**
   - nmake 명령어 필요
   - https://visualstudio.microsoft.com/downloads/

2. **pg_config 경로 설정**
   ```batch
   set PATH=%PGROOT%\bin;%PATH%
   ```

3. **Makefile.win 존재 확인**
   - pgvector 소스에 Makefile.win 이 있는지 확인 필요

## 더 쉬운 방법

### 방법 1: Docker 사용 (권장)

```dockerfile
# pgvector 포함 PostgreSQL
FROM pgvector/pgvector:pg18
```

```bash
docker run -d \
  -e POSTGRES_PASSWORD=mypassword \
  -p 5432:5432 \
  pgvector/pgvector:pg18
```

### 방법 2: PostgreSQL Extension 으로 설치

```sql
-- PostgreSQL 에 연결
psql -U postgres -d your_database

-- pgvector 설치 시도
CREATE EXTENSION IF NOT EXISTS vector;
```

### 방법 3: WSL2 사용

```bash
# WSL2 에서 설치
sudo apt update
sudo apt install postgresql-18 postgresql-server-dev-18

# pgvector 설치
cd /tmp
git clone --branch v0.8.2 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

## 확인 방법

```sql
-- pgvector 설치 확인
SELECT * FROM pg_extension WHERE extname = 'vector';

-- 벡터 타입 테스트
CREATE TABLE test (v vector(3));
INSERT INTO test VALUES ('[1,2,3]');
SELECT * FROM test;
```
