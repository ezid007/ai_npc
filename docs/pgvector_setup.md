# pgvector 설치 가이드 (Windows)

## PostgreSQL 확인

```powershell
# PostgreSQL 설치 위치 확인
Get-ChildItem "C:\Program Files\PostgreSQL" -Recurse -Filter "psql.exe"
```

## pgvector 설치 방법

### 방법 1: 공식 바이너리 설치 (권장)

1. **pgvector 릴리스 페이지 방문**
   - https://github.com/pgvector/pgvector/releases

2. **Windows 바이너리 다운로드**
   - PostgreSQL 버전 확인 (예: PostgreSQL 18)
   - 해당 버전의 Windows 설치 프로그램 다운로드

3. **설치**
   ```powershell
   # 설치 프로그램 실행
   .\pgvector-windows-installer.exe
   ```

### 방법 2: SQL 로 확장 기능 생성

```sql
-- PostgreSQL 에 연결
psql -U postgres -d your_database

-- pgvector 확장 생성
CREATE EXTENSION IF NOT EXISTS vector;
```

### 방법 3: 소스 컴파일

```bash
# Git 설치 필요
git clone https://github.com/pgvector/pgvector.git
cd pgvector

# PostgreSQL 개발 파일 필요
# Windows 에서는 MSYS2 또는 WSL 사용 권장

# 컴파일
make
make install
```

## 설치 확인

```sql
-- PostgreSQL 연결
psql -U postgres -d your_database

-- pgvector 설치 확인
SELECT * FROM pg_extension WHERE extname = 'vector';

-- 벡터 타입 테스트
CREATE TABLE test_vectors (
    id SERIAL PRIMARY KEY,
    embedding vector(3)
);

INSERT INTO test_vectors (embedding) VALUES ('[1,2,3]');
SELECT * FROM test_vectors;

-- 유사도 검색 테스트
INSERT INTO test_vectors (embedding) VALUES ('[4,5,6]');
SELECT embedding <-> '[1,2,3]' AS distance FROM test_vectors;
```

## Python 설정

### 1. 의존성 설치

```bash
pip install psycopg2-binary pgvector
```

### 2. 벡터 타입 등록

```python
from pgvector.psycopg2 import register_vector
import psycopg2

# 데이터베이스 연결
conn = psycopg2.connect(
    host="localhost",
    database="your_database",
    user="postgres",
    password="your_password"
)

# 벡터 타입 등록
register_vector(conn)

# 사용 예시
cur = conn.cursor()
cur.execute("CREATE TABLE documents (id SERIAL PRIMARY KEY, content TEXT, embedding vector(1536))")
```

## 환경 변수 설정

`.env` 파일에 PostgreSQL 설정 추가:

```env
# PostgreSQL 설정
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_npc_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

## 문제 해결

### "vector" 타입을 찾을 수 없음

```sql
-- pgvector 확장 설치 확인
SELECT * FROM pg_extension;

-- 설치되어 있지 않으면
CREATE EXTENSION vector;
```

### 연결 오류

```python
# 연결 테스트
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="your_db",
        user="postgres",
        password="your_password"
    )
    print("Connected!")
except Exception as e:
    print(f"Error: {e}")
```

## 참고 자료

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [pgvector 문서](https://github.com/pgvector/pgvector#installation)
- [pgvector Python](https://github.com/pgvector/pgvector-python)
