# pgvector 학습 가이드

## 목차
1. [pgvector 란?](#1-pgvector-란)
2. [설치](#2-설치)
3. [기본 사용법](#3-기본-사용법)
4. [벡터 저장](#4-벡터-저장)
5. [유사도 검색](#5-유사도-검색)
6. [인덱싱](#6-인덱싱)
7. [Python 연동](#7-python-연동)
8. [RAG 적용](#8-rag-적용)

---

## 1. pgvector 란?

pgvector 는 PostgreSQL 에 벡터 유사도 검색 기능을 추가하는 오픈소스 확장 프로그램입니다.

**주요 기능:**
- 정확한 및 근사 nearest neighbor 검색
- 단일 정밀도, 반 정밀도, 이진, 희소 벡터 지원
- L2 거리, 내적, 코사인 거리, L1 거리, 해밍 거리, 자카드 거리 지원
- ACID 준수, 포인트 인 타임 리커버리, JOIN 등 PostgreSQL 모든 기능과 호환

---

## 2. 설치

### 2.1 사전 요구사항
- PostgreSQL 13 이상
- Visual Studio 2022 (Windows 빌드용)

### 2.2 Windows 설치

```cmd
# Visual Studio x64 Native Tools Command Prompt 실행
set "PGROOT=C:\Program Files\PostgreSQL\18"
cd %TEMP%
git clone https://github.com/pgvector/pgvector.git
cd pgvector
nmake /F Makefile.win
nmake /F Makefile.win install
```

### 2.3 확장 생성

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2.4 설치 확인

```sql
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
```

---

## 3. 기본 사용법

### 3.1 벡터 컬럼 생성

```sql
-- 3 차원 벡터 테이블 생성
CREATE TABLE items (
    id BIGSERIAL PRIMARY KEY,
    embedding VECTOR(3)
);
```

### 3.2 벡터 삽입

```sql
INSERT INTO items (embedding) VALUES 
    ('[1,2,3]'),
    ('[4,5,6]');
```

### 3.3 유사도 검색

```sql
-- L2 거리로 가장 가까운 이웃 찾기
SELECT * FROM items 
ORDER BY embedding <-> '[3,1,2]' 
LIMIT 5;
```

---

## 4. 벡터 저장

### 4.1 새 테이블 생성

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(1536)  -- 임베딩 차원 수 (모델에 따라 다름)
);
```

### 4.2 기존 테이블에 벡터 컬럼 추가

```sql
ALTER TABLE documents ADD COLUMN embedding VECTOR(1536);
```

### 4.3 벡터 삽입

```sql
-- 단일 삽입
INSERT INTO documents (content, embedding) 
VALUES ('문서 내용', '[0.1, 0.2, 0.3, ...]');

-- 대량 삽입 (COPY)
COPY documents (embedding) FROM STDIN WITH (FORMAT BINARY);
```

### 4.4 벡터 업데이트

```sql
UPDATE documents SET embedding = '[1,2,3]' WHERE id = 1;
```

### 4.5 벡터 삭제

```sql
DELETE FROM documents WHERE id = 1;
```

---

## 5. 유사도 검색

### 5.1 거리 함수

| 연산자 | 거리 함수 | 설명 |
|--------|-----------|------|
| `<->` | L2 거리 | 유클리드 거리 |
| `<#>` | (음수) 내적 | Inner Product |
| `<=>` | 코사인 거리 | Cosine Distance |
| `<+>` | L1 거리 | Manhattan 거리 |
| `<~>` | 해밍 거리 | 이진 벡터 |
| `<%>` | 자카드 거리 | 이진 벡터 |

### 5.2 가장 가까운 이웃 찾기

```sql
SELECT * FROM items 
ORDER BY embedding <-> '[3,1,2]' 
LIMIT 5;
```

### 5.3 행 단위 가장 가까운 이웃

```sql
SELECT * FROM items 
WHERE id != 1 
ORDER BY embedding <-> (SELECT embedding FROM items WHERE id = 1) 
LIMIT 5;
```

### 5.4 특정 거리 이내의 행 찾기

```sql
SELECT * FROM items 
WHERE embedding <-> '[3,1,2]' < 5;
```

### 5.5 거리 계산

```sql
-- L2 거리
SELECT embedding <-> '[3,1,2]' AS distance FROM items;

-- 내적 (음수 * -1)
SELECT (embedding <#> '[3,1,2]') * -1 AS inner_product FROM items;

-- 코사인 유사도 (1 - 코사인 거리)
SELECT 1 - (embedding <=> '[3,1,2]') AS cosine_similarity FROM items;
```

---

## 6. 인덱싱

### 6.1 기본 검색

기본적으로 pgvector 는 정확한 nearest neighbor 검색을 수행합니다.

### 6.2 HNSW 인덱스

더 빠른 검색을 위해 HNSW 인덱스를 생성할 수 있습니다.

```sql
-- L2 거리 인덱스
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);

-- 코사인 거리 인덱스
CREATE INDEX ON items USING hnsw (embedding vector_cosine_ops);

-- 내적 인덱스
CREATE INDEX ON items USING hnsw (embedding vector_ip_ops);
```

### 6.3 HNSW 파라미터

```sql
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops) 
WITH (m = 16, ef_construction = 64);
```

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| `m` | 레이어당 최대 연결 수 | 16 |
| `ef_construction` | 그래프 구축을 위한 후보 리스트 크기 | 64 |

### 6.4 검색 파라미터

```sql
-- 검색 정확도 설정 (기본값: 40)
SET hnsw.ef_search = 100;

-- 트랜잭션 내에서만 적용
BEGIN;
SET LOCAL hnsw.ef_search = 100;
SELECT ...;
COMMIT;
```

### 6.5 인덱스 진행 상황 확인

```sql
SELECT phase, round(100.0 * blocks_done / nullif(blocks_total, 0), 1) AS "%" 
FROM pg_stat_progress_create_index;
```

---

## 7. Python 연동

### 7.1 의존성 설치

```bash
pip install psycopg2-binary pgvector
```

### 7.2 벡터 타입 등록

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
```

### 7.3 벡터 삽입

```python
import numpy as np

# 임베딩 생성 (예: 1536 차원)
embedding = np.random.rand(1536).tolist()

# 삽입
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
    ("문서 내용", embedding)
)
conn.commit()
```

### 7.4 유사도 검색

```python
query_embedding = np.random.rand(1536).tolist()

cursor.execute(
    """
    SELECT content, embedding <-> %s AS distance 
    FROM documents 
    ORDER BY distance 
    LIMIT 5
    """,
    (query_embedding,)
)

results = cursor.fetchall()
for content, distance in results:
    print(f"{content}: {distance}")
```

---

## 8. RAG 적용

### 8.1 RAG 아키텍처

```
1. 문서 → 임베딩 → pgvector 저장
2. 질문 → 임베딩 → pgvector 검색
3. 검색된 문서 + 질문 → LLM → 답변
```

### 8.2 문서 임베딩 저장

```python
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import PGVector

# 임베딩 모델
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# PGVector 연결
vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="documents",
    connection_string="postgresql://postgres:password@localhost:5432/your_database"
)

# 문서 추가
vectorstore.add_documents(documents)
```

### 8.3 유사도 검색

```python
# 질문 기반 검색
relevant_docs = vectorstore.similarity_search("질문 내용", k=5)

for doc in relevant_docs:
    print(doc.page_content)
```

### 8.4 RAG 파이프라인

```python
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceLLM

# LLM 설정
llm = HuggingFaceLLM(model_name="your-llm-model")

# RAG 체인
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

# 질문
response = qa_chain.invoke("질문 내용")
print(response["result"])
```

---

## 9. 성능 최적화

### 9.1 메모리 설정

```sql
-- 인덱스 빌드 속도 향상
SET maintenance_work_mem = '8GB';

-- 병렬 작업자 증가
SET max_parallel_maintenance_workers = 7;
```

### 9.2 인덱스 생성 타이밍

- 초기 데이터 로드 후 인덱스 생성 권장
- 대량 삽입 시 인덱스 생성 지연

### 9.3 검색 정확도 vs 속도

```sql
-- 정확도 높음 (속도 느림)
SET hnsw.ef_search = 100;

-- 속도 높음 (정확도 낮음)
SET hnsw.ef_search = 20;
```

---

## 10.常见问题

### 10.1 벡터 차원 수 변경

```sql
-- 테이블 삭제 후 재생성 (데이터 백업 필요)
DROP TABLE items;
CREATE TABLE items (id BIGSERIAL PRIMARY KEY, embedding VECTOR(1536));
```

### 10.2 인덱스 재구축

```sql
DROP INDEX IF EXISTS items_embedding_idx;
CREATE INDEX ON items USING hnsw (embedding vector_l2_ops);
```

### 10.3 확장 제거

```sql
DROP EXTENSION IF EXISTS vector;
```

---

## 참고 자료

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [pgvector Releases](https://github.com/pgvector/pgvector/releases)
- [LangChain PGVector](https://python.langchain.com/docs/integrations/vectorstores/pgvector)
