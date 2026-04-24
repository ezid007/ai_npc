 # RAG (Retrieval-Augmented Generation) 가이드

## RAG 란?

RAG(Retrieval-Augmented Generation, 검색 증강 생성) 는 LLM 이 외부 지식을 활용하여 더 정확하고 관련성 높은 응답을 생성할 수 있게 하는 아키텍처입니다.

### 기본 개념

```
사용자 질문 → [검색] → 관련 문서 → [생성] → 답변
                ↓            ↓
           벡터 DB      LLM 과 결합
```

---

## 왜 RAG 가 필요한가?

### LLM 의 한계

1. **학습 데이터 기준일 뿐 최신 정보 모름**
    - LLM 은 학습 시점 이후의 정보를 알 수 없음
    - 예: 2024 년 학습 모델은 2025 년 뉴스 모름

2. **특정 도메인 지식 부족**
    - 게임 세계관, 회사 내부 문서 등 특정 지식 부족

3. **할루시네이션 (거짓 정보 생성) 문제**
    - 없는 사실을 만들어낼 수 있음

### RAG 의 해결

1. **실시간/최신 정보 활용 가능**
2. **도메인 특화 지식 추가 가능**
3. **출처 기반 답변으로 신뢰도 향상**

---

## RAG 의 핵심 구성 요소

### 1. 문서 처리 파이프라인

```
원본 문서 → 분할 → 임베딩 → 벡터 DB 저장
```

#### 문서 분할 (Chunking)

문서를 적절한 크기로 나눕니다.

- **고정 크기**: 예: 500 토큰씩 분할
- **슬라이딩 윈도우**: 중첩 포함하여 분할
- **문장/단위 기반**: 문장, 단락 단위 분할

#### 임베딩 (Embedding)

텍스트를 벡터로 변환합니다.

- **Microsoft Harrier OSS v1 0.6B**: 다국어 임베딩 모델
    - 임베딩 차원: 1,024
    - 한국어 지원
    - 지시어 (instruction) 기반 쿼리 처리
- **Sentence Transformers**: 로컬 임베딩 모델
- **OpenAI Embeddings**: 클라우드 기반

### 2. 벡터 데이터베이스

텍스트를 벡터로 변환하여 저장하고 유사도 검색을 수행합니다.

| DB           | 특징                  | 사용 사례   |
| ------------ | --------------------- | ----------- |
| **pgvector** | PostgreSQL 확장, ACID | 프로덕션    |
| **Chroma**   | 로컬, 경량            | 개발/테스트 |
| **Pinecone** | 클라우드, 관리형      | 프로덕션    |
| **Milvus**   | 오픈소스, 확장성      | 대규모      |
| **FAISS**    | Facebook, 고속        | 대량 검색   |

### 3. 검색 (Retrieval)

사용자 쿼리와 저장된 문서의 유사도를 계산하여 관련 문서를 찾습니다.

- **유사도 계산**: 코사인 유사도, 내적 등
- **검색 방식**:
    - **Dense Retrieval**: 벡터 기반 검색
    - **Hybrid Search**: 벡터 + 키워드 (BM25) 결합 (권장)

### 4. 생성 (Generation)

검색된 문서를 LLM 에게 제공하여 답변을 생성합니다.

```
시스템: "다음 문서를 참고하여 답변하세요."
문서: "[검색된 문서 내용]"
사용자: "[질문]"
→ LLM 응답
```

---

## RAG 작동 흐름

### 문서 저장 단계

```
1. 원본 문서 준비
   ↓
2. 문서 분할 (Chunking)
   - 고정 크기 / 슬라이딩 윈도우 / 문장 단위
   ↓
3. 문서 임베딩 생성
   - 모델: Microsoft Harrier OSS v1 0.6B
   - 지시어 포함 안 함 (문서만 입력)
   ↓
4. pgvector 에 저장
   - content: 원본 텍스트
   - embedding: 1,024 차원 벡터
```

### 검색 및 생성 단계

```
5. 사용자 질문 입력
   ↓
6. 질문 임베딩 생성
   - 모델: Microsoft Harrier OSS v1 0.6B (같은 모델 사용)
   - 지시어 포함: "Instruct: [작업 설명]\nQuery: [질문]"
   ↓
7. 유사 문서 검색 (pgvector)
   - 내적 (<#>) 또는 코사인 거리 (<=>) 사용
   - Top-K 문서 반환
   ↓
8. 문맥 구성 (Prompt)
   시스템: "다음 문서를 참고하여 답변하세요."
   문서: "[검색된 문서 내용]"
   사용자: "[질문]"
   ↓
9. LLM 에게 전송
   - vLLM 서버 (RedHatAI/Qwen3.5-122B-A10B-NVFP4)
   ↓
10. 답변 생성
```

### 중요 포인트

| 단계 | 모델 | 지시어 |
|------|------|--------|
| **문서 임베딩** | harrier-oss-v1-0.6b | ❌ 없음 |
| **쿼리 임베딩** | harrier-oss-v1-0.6b | ✅ 포함 |

**같은 임베딩 모델을 사용해야** 쿼리와 문서가 같은 벡터 공간에 매핑되어 유사도 계산이 가능합니다.

---

## RAG 의 장점

1. **정확도 향상**: 사실 기반 답변
2. **최신성**: 실시간 정보 반영
3. **도메인 특화**: 커스텀 지식 추가
4. **설명 가능성**: 출처 명시 가능
5. **유연성**: 모델 재학습 없이 지식 추가

---

## RAG 의 단점 및 해결책

| 문제              | 해결책                    |
| ----------------- | ------------------------- |
| **부적절한 검색** | Hybrid Search, Re-ranking |
| **문맥 초과**     | 문장 분할, 중요도 필터링  |
| **지연 시간**     | 캐싱, 최적화된 DB         |
| **비용**          | 효율적 임베딩 선택        |

---

## LangChain (Python 프레임워크)

RAG 구현을 위해 **LangChain** 프레임워크를 사용할 수 있습니다.

### LangChain 이란?

LangChain 은 LLM(대형 언어 모델) 을 사용하여 애플리케이션을 구축하기 위한 **Python 프레임워크**입니다.

### RAG 파이프라인에서의 역할

| 단계 | LangChain 기능 | 설명 |
|------|----------------|------|
| **문서 분할** | `TextSplitter` | 문서를 적절한 크기로 분할 |
| **임베딩** | `Embeddings` | 임베딩 모델 연결 (Harrier 등) |
| **벡터 저장** | `VectorStore` | pgvector, Chroma 등 연결 |
| **검색** | `Retriever` | 유사 문서 검색 |
| **문맥 구성** | `PromptTemplate` | 검색된 문서로 프롬프트 구성 |
| **LLM 연동** | `LLM` | vLLM, OpenAI 등 연결 |
| **체인** | `RetrievalQA` | 전체 파이프라인 연결 |

### LangChain 사용 예시

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import PGVector
from langchain.chains import RetrievalQA
from langchain_community.llms import VLLM

# 1. 문서 분할
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.split_text(raw_text)

# 2. 임베딩 (Harrier 모델 사용 시 커스텀 필요)
embeddings = HuggingFaceEmbeddings(model_name="microsoft/harrier-oss-v1-0.6b")

# 3. 벡터 저장 (pgvector)
vectorstore = PGVector(
    embeddings=embeddings,
    collection_name="documents",
    connection_string="postgresql://postgres:password@localhost:5432/your_db"
)
vectorstore.add_texts(documents)

# 4. 검색 (Retriever)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 5. LLM 연동 (vLLM)
llm = VLLM(
    model="RedHatAI/Qwen3.5-122B-A10B-NVFP4",
    base_url="http://192.168.1.83:28000/v1"
)

# 6. 체인 연결
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 7. 질문
response = qa_chain.invoke("프로테인 파우더 추천해줘")
print(response["result"])
```

---

## AI NPC 프로젝트에서의 RAG 적용

NPC 에게 다음과 같은 지식을 제공할 수 있습니다:

1. **게임 세계관**: 로어, 배경 스토리
2. **퀘스트 정보**: 퀘스트 조건, 보상
3. **NPC 페르소나**: 성격, 대화 스타일
4. **사용자 기억**: 이전 대화 기록
5. **게임 상태**: 현재 상황, 이벤트

---

## 구현 단계

### 1 단계: 벡터 DB 설정

- **PostgreSQL + pgvector** 로 벡터 데이터베이스 구축
    - PostgreSQL 18 설치
    - pgvector 확장 설치 (v0.8.2)
    - `CREATE EXTENSION vector;`로 활성화
- **임베딩 모델**: Microsoft Harrier OSS v1 0.6B
    - 모델: `microsoft/harrier-oss-v1-0.6b`
    - 임베딩 차원: 1,024
    - 다국어 지원 (한국어 포함)
    - MTEB v2 Score: 69.0

### 2 단계: 문서 처리

- 문서 분할 로직 구현
- 임베딩 변환 및 저장

### 3 단계: 검색 구현

- **유사도 검색 구현**: 벡터 기반 검색
- **Hybrid Search**: 벡터 + 키워드 검색 결합 (권장)
  - **벡터 검색**: 의미 기반 검색 (문맥 이해)
  - **키워드 검색 (BM25)**: 정확한 단어 매칭
  - **결합**: 두 검색 결과의 점수를 가중치로 합산
- Top-K 문서 반환

### 4 단계: LLM 연동

- 검색된 문서로 문맥 구성
- LLM 에게 전송 및 응답 받기

### 5 단계: 최적화

- Hybrid Search 추가
- 캐싱 구현
- 성능 튜닝

---

## 참고 자료

- [LangChain RAG 가이드](https://python.langchain.com/docs/use_cases/qa_chating/)
- [LlamaIndex RAG 가이드](https://docs.llamaindex.ai/en/stable/getting_started/starter_example_local/)
- [pgvector 문서](https://github.com/pgvector/pgvector)
- [Microsoft Harrier 모델](https://huggingface.co/microsoft/harrier-oss-v1-0.6b)
