# 스마일게이트 AI NPC 개발자 포지션 기술 스택

## 📋 포지션 개요

**회사:** 스마일게이트  
**위치:** 경기 성남시 분당구 판교로 344 (삼평동) 스마일게이트 캠퍼스  
**마감일:** 2026.05.16

### 주요 업무
- 페르소나/환경/대화 히스토리/기억을 통합한 AI NPC 발화·행동 생성 엔진 개발
- 게임 지식과 NPC 경험 기반 장·단기 기억 저장 및 색인·추출 알고리즘 연구
- 심리/감정/의도 추론 기반 NPC 자율 발화 및 의사결정 모델 개발
- LLM 기반 NPC 대화 모델 Fine-tuning, Prompt Engineering, RLHF 적용을 통한 대화 성능 향상

### 자격요건
- RAG 및 LLM 기반 지능형 에이전트/대화 시스템 설계 및 개발 경험
- 언어모델 Fine-tuning, Prompt Engineering, RLHF 등 최신 기법을 활용한 모델 커스터마이징 및 성능 최적화 경험
- AI 시스템 아키텍처 설계 및 대화형 인터페이스 구현 경험

---

## 🛠️ 핵심 기술 스택

### 1. LLM (Large Language Model)

| 기술 | 설명 | 학습 자료 |
|------|------|----------|
| **LLM 기본기** | GPT, Llama, Claude 등 모델 이해 | Transformer 아키텍처, Attention Mechanism |
| **OpenAI API** | GPT-4, GPT-3.5 활용 | Chat Completions, Function Calling |
| **오픈소스 LLM** | Llama 3, Mistral, Qwen | Hugging Face Transformers |
| **모델 배포** | vLLM, TGI, TensorRT-LLM | 로컬/클라우드 배포 |

### 2. RAG (Retrieval-Augmented Generation)

| 기술 | 설명 | 라이브러리/도구 |
|------|------|----------------|
| **벡터 데이터베이스** | 문서/기억 저장 및 검색 | Pinecone, Weaviate, Milvus, Chroma |
| **임베딩** | 텍스트를 벡터로 변환 | OpenAI Embeddings, Sentence Transformers, BGE |
| **검색 알고리즘** | 유사도 검색, Hybrid Search | FAISS, BM25, Dense Retrieval |
| **RAG 프레임워크** | 엔드투엔드 파이프라인 | LangChain, LlamaIndex, Haystack |

### 3. Fine-tuning (모델 미세 조정)

| 기술 | 설명 | 도구/프레임워크 |
|------|------|----------------|
| **Full Fine-tuning** | 전체 파라미터 조정 | Hugging Face Trainer, DeepSpeed |
| **PEFT (Parameter-Efficient)** | 효율적 미세조정 | LoRA, QLoRA, Adapter |
| **데이터 준비** | 학습 데이터 생성/정제 | Datasets, Pandas, Custom Pipeline |
| **분산 학습** | 대규모 모델 학습 | PyTorch Distributed, FSDP, DeepSpeed |

### 4. Prompt Engineering

| 기술 | 설명 | 기법 |
|------|------|------|
| **기본 프롬프트** | Zero-shot, Few-shot | 명확한 지시, 컨텍스트 제공 |
| **고급 기법** | Chain-of-Thought, ReAct | 단계적 추론, 도구 사용 |
| **시스템 프롬프트** | 페르소나/역할 정의 | NPC 성격, 배경 설정 |
| **프롬프트 최적화** | A/B 테스트, 자동화 | DSPy, PromptOptimization |

### 5. RLHF (Reinforcement Learning from Human Feedback)

| 기술 | 설명 | 라이브러리 |
|------|------|-----------|
| **RL 기본기** | PPO, DDPG, SAC | Stable Baselines3, RLlib |
| **RLHF 파이프라인** | Reward Modeling, PPO | TRL (Transformer Reinforcement Learning) |
| **Human Feedback** | 선호도 데이터 수집 | Label Studio, Custom UI |
| **DPO (Direct Preference Optimization)** | RLHF 대안 | DPO Implementation |

### 6. 대화 시스템 (Conversational AI)

| 기술 | 설명 | 프레임워크 |
|------|------|-----------|
| **다중턴 대화** | 컨텍스트 유지 | LangChain Memory, Custom Store |
| **상태 관리** | 대화 상태 추적 | FSM, State Machine |
| **감정/심리 모델** | NPC 감정 상태 | Custom Emotion Engine, Unity ML-Agents |
| **행동 생성** | 발화 + 행동 연동 | Game Engine Integration |

### 7. 게임 엔진 통합

| 기술 | 설명 | 플랫폼 |
|------|------|--------|
| **언리얼 엔진** | NPC AI 통합 | Blueprint, C++, Python API |
| **Unity** | 대안 엔진 | C#, ML-Agents |
| **네트워킹** | 멀티플레이 동기화 | Replication, Authority |
| **성능 최적화** | 실시간 응답 | Async Processing, Caching |

---

## 💻 프로그래밍 언어

| 언어 | 사용 목적 | 숙련도 |
|------|----------|-------|
| **Python** | AI/ML 개발, API | **상급** (필수) |
| **C++** | 게임 엔진 통합 | **중급 이상** (권장) |
| **C#** | Unity 통합 | **중급** (선택) |
| **SQL** | 데이터베이스 | **중급** |

---

## 🏗️ 인프라/배포

| 기술 | 설명 | 도구 |
|------|------|------|
| **컨테이너** | 애플리케이션 패키징 | Docker, Kubernetes |
| **클라우드** | 모델/서비스 배포 | AWS, GCP, Azure |
| **API 개발** | REST/GraphQL | FastAPI, Flask, GraphQL |
| **모니터링** | 성능/로그 | Prometheus, Grafana, ELK |

---

## 📚 학습 로드맵 (추천 순서)

```
1 단계 (기초): Python → PyTorch → Transformer 이해
2 단계 (LLM): Hugging Face → OpenAI API → Prompt Engineering
3 단계 (RAG): 벡터 DB → LangChain → 검색 최적화
4 단계 (Fine-tuning): LoRA/QLoRA → 학습 파이프라인
5 단계 (RLHF): Reward Modeling → PPO → DPO
6 단계 (통합): 게임 엔진 연동 → 실시간 시스템
```

### 상세 학습 기간

| 단계 | 내용 | 예상 기간 |
|------|------|----------|
| **1 단계** | Python, PyTorch, Transformer 기초 | 2 주 |
| **2 단계** | Hugging Face, OpenAI API, Prompt Engineering | 2 주 |
| **3 단계** | 벡터 DB, LangChain, RAG 구현 | 2 주 |
| **4 단계** | LoRA/QLoRA 파인튜닝 | 2 주 |
| **5 단계** | RLHF, DPO | 2 주 |
| **6 단계** | 게임 엔진 연동, 프로덕트 개발 | 4 주 |

**총 예상 기간: 14 주 (약 3.5 개월)**

---

## 🎯 스마일게이트 포지션 특화 준비

| 영역 | 준비 사항 |
|------|----------|
| **NPC 페르소나** | 캐릭터 설정, 배경 스토리, 성격 모델링 |
| **기억 시스템** | 장기/단기 기억 구조, 색인/검색 알고리즘 |
| **감정 모델** | 감정 상태 전이, 표현 방식 |
| **게임 지식** | MMORPG 시스템, NPC 역할 이해 |

---

## 💼 포트폴리오 추천

### 필수 프로젝트

1. **RAG 기반 챗봇**
   - LangChain + 벡터 DB (Chroma/Pinecone)
   - 문서 기반 질문 응답 시스템

2. **LLM Fine-tuning 프로젝트**
   - LoRA/QLoRA 적용
   - 커스텀 데이터셋으로 학습

3. **NPC 대화 시스템 데모**
   - Unreal Engine 또는 Unity 연동
   - 페르소나 기반 대화 생성

### 선택 프로젝트

4. **감정/상태 기반 AI 에이전트**
   - 감정 상태 전이 모델
   - 상황에 따른 응답 변화

5. **RLHF 파이프라인**
   - 선호도 데이터 수집 UI
   - DPO/PPO 적용

---

## 📖 추천 학습 자료

### 문서/가이드
- [LangChain 공식 문서](https://python.langchain.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [LlamaIndex 공식 문서](https://docs.llamaindex.ai/)

### 강의/튜토리얼
- Hugging Face NLP Course (무료)
- LangChain for LLM Application (Coursera)
- DeepLearning.AI RAG 강의

### GitHub 리포지토리
- [langchain-ai/langchain](https://github.com/langchain-ai/langchain)
- [huggingface/peft](https://github.com/huggingface/peft)
- [ludwig-ai/ludwig](https://github.com/ludwig-ai/ludwig)

---

## ✅ 체크리스트

### 기초 기술
- [ ] Python 숙련도 (Async, Decorator, Generator)
- [ ] PyTorch 기본기 (Tensor, Autograd, Dataset)
- [ ] Transformer 아키텍처 이해

### LLM/생성 AI
- [ ] OpenAI API 사용 경험
- [ ] 오픈소스 LLM 실행 경험 (Llama, Mistral)
- [ ] Prompt Engineering 기법

### RAG
- [ ] 벡터 DB 사용 경험 (Chroma, Pinecone 등)
- [ ] LangChain 또는 LlamaIndex 사용 경험
- [ ] 임베딩 모델 이해

### Fine-tuning
- [ ] LoRA/QLoRA 적용 경험
- [ ] 학습 데이터 준비/정제
- [ ] 모델 평가/최적화

### RLHF
- [ ] PPO 기본 이해
- [ ] Reward Modeling
- [ ] DPO 구현 경험

### 게임 통합
- [ ] Unreal Engine Python API
- [ ] 실시간 시스템 설계
- [ ] 성능 최적화

---

## 📞 추가 정보

**문의:** 스마일게이트 채용 페이지  
**지원 링크:** https://www.wanted.co.kr/wd/329539

---

*최종 업데이트: 2026 년 4 월 8 일*
