# AI NPC 프로젝트

AI NPC (Non-Player Character) 개발을 위한 학습 및 개발 프로젝트

## 📋 프로젝트 개요

이 프로젝트는 AI NPC 시스템 개발을 위한 기술 스택 기반 학습 및 개발 환경입니다.

- **LLM**: 외부 vLLM 서버 (OpenAI Compatible) 연결
- **주요 기술**: RAG, Fine-tuning, Prompt Engineering, RLHF
- **목표**: AI NPC 대화 시스템 개발 및 게임 엔진 통합
- **환경**: CUDA/GPU 불필요 - 외부 서버만 사용

## 🏗️ 프로젝트 구조

```
ai_npc/
├── src/                    # 소스 코드
│   ├── __init__.py
│   ├── llm_client.py       # vLLM API 클라이언트
│   ├── conversation.py     # NPC 대화 시스템
│   └── test_llm_stream.py  # 스트리밍 테스트
├── .env                    # 환경 변수 (API 키 등)
├── .env.example            # 환경 변수 예시
├── requirements.txt        # Python 의존성
└── README.md
```

## 🏛️ 전체 구성도

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        🖥️ 노트북 (로컬 개발 환경)                            │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  AI NPC 클라이언트 (conversation.py)                                   │  │
│  │  - RAG 엔진                                                            │  │
│  │  - 벡터 DB (PostgreSQL + pgvector)                                     │  │
│  │  - 문서 처리 (임베딩/분할)                                             │  │
│  │  - .env (VLLM_API_BASE, VLLM_API_KEY)                                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                    │                                         │
│                                    │ HTTP/OpenAI Compatible API              │
│                                    ▼                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ 동일 네트워크
                                    │
┌─────────────────────────────────────────────────────────────────────────────┐
│                    🖥️ DGX 스파크 (vLLM 서버)                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  vLLM 서버 (OpenAI Compatible API)                                     │  │
│  │  - LLM 인퍼런스 (Qwen3.5 등)                                           │  │
│  │  - 스트리밍 응답                                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 데이터 흐름

```
사용자 입력
    │
    ▼
┌─────────────────┐
│ RAG 엔진        │ ────► 벡터 DB 검색 (PostgreSQL + pgvector)
└─────────────────┘         │
    │                       ▼
    │              ┌─────────────────┐
    └─────────────►│ 관련 문서 검색   │
                   └─────────────────┘
                           │
                           ▼
                   ┌─────────────────┐
                   │ 컨텍스트 구성    │
                   └─────────────────┘
                           │
                           ▼ (HTTP API)
┌─────────────────────────────────────────┐
│  DGX 스파크 - vLLM 서버                 │
│  ┌───────────────────────────────────┐  │
│  │  LLM 추론 (Qwen3.5)               │  │
│  │  ───────────────────────────────  │  │
│  │  스트리밍 응답                    │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                           │
                           ▼
                   ┌─────────────────┐
                   │ 최종 응답        │
                   └─────────────────┘
```

## 🌐 네트워크 구성

| 구성 요소  | 역할                           | 위치           |
| ---------- | ------------------------------ | -------------- |
| 노트북     | RAG 처리, 클라이언트 실행      | 로컬 개발 환경 |
| DGX 스파크 | vLLM 서버 구동, LLM 인퍼런스   | 동일 네트워크  |
| 연결 방식  | OpenAI Compatible API (HTTP)   | 내부 네트워크  |
| 보안       | API 키 기반 인증 (`.env` 관리) | 로컬           |

## 🚀 시작하기

### 1. 가상환경 생성 및 활성화

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 값을 설정하세요:

```env
VLLM_API_BASE=your-vllm-server-url
VLLM_API_KEY=your-api-key
VLLM_MODEL_NAME=your-model-name
```

**중요:** `.env` 파일의 값을 실제 설정으로 변경해야 합니다.

- `VLLM_API_BASE`: vLLM 서버 주소 (예: `http://localhost:8000/v1`)
- `VLLM_API_KEY`: API 키 (로컬 서버는 빈 값 가능)
- `VLLM_MODEL_NAME`: vLLM 에서 로드된 모델 이름

### 4. 실행 테스트

```bash
python src/conversation.py
```

## 📖 학습 로드맵

1. **LLM 기본기**: Transformer, Attention Mechanism
2. **vLLM API**: OpenAI Compatible API 사용법
3. **RAG**: 벡터 DB, 임베딩, 검색
4. **Fine-tuning**: LoRA, QLoRA
5. **RLHF**: Reward Modeling, PPO
6. **게임 엔진 통합**: Unreal Engine, Unity

## 🔧 기술 스택

- **LLM**: vLLM (OpenAI Compatible API)
- **Vector DB**: PostgreSQL + pgvector
- **RAG**: 임베딩, 벡터 검색, 문서 분할
- **Fine-tuning**: LoRA, QLoRA
- **Platform**: Windows (PowerShell, Visual Studio Build Tools)
