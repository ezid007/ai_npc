"""
AI NPC 프로젝트 - vLLM API 클라이언트 모듈

이 모듈은 vLLM 서버 (OpenAI Compatible) 와 통신하기 위한 클라이언트를 제공합니다.
vLLM 은 오픈소스 LLM 서빙 라이브러리로, 로컬 또는 사설 서버에서 LLM 을 실행할 때 사용됩니다.

사용 방법:
    1. .env 파일에 VLLM_API_BASE, VLLM_API_KEY, VLLM_MODEL_NAME 설정
    2. LLMClient 인스턴스 생성
    3. chat() 또는 generate() 메서드 호출

중요: 모든 설정은 .env 파일에서 관리됩니다. 코드에 디폴트 값은 존재하지 않습니다.
"""

import os
import sys
from typing import List, Dict, Any, Optional, Union

# dotenv 명시적 로드 - .env 파일에서 환경 변수 로드
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import httpx

# .env 파일 로드 (프로젝트 루트의 .env 파일 명시적 로드)
from pathlib import Path

# 프로젝트 루트 경로를 기준으로 .env 파일 로드
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class LLMClient:
    """
    vLLM API 클라이언트 클래스

    OpenAI API 호환 인터페이스를 사용하여 vLLM 서버와 통신합니다.
    모든 설정 (.env) 에서 로드됩니다.

    Attributes:
        client (OpenAI): OpenAI API 클라이언트 인스턴스
        model (str): 사용할 모델 이름
        base_url (str): vLLM 서버 URL
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 300.0,  # 5 분으로 증가 (122B 모델용)
        max_retries: int = 3,
    ):
        """
        LLMClient 초기화

        Args:
            api_key: vLLM API 키 (없으면 .env 에서 자동 로드)
            base_url: vLLM 서버 URL (없으면 .env 에서 자동 로드)
            model: 사용할 모델 이름 (없으면 .env 에서 자동 로드)
            timeout: API 요청 타임아웃 (초)
            max_retries: 최대 재시도 횟수
        """
        # 환경 변수에서 값 로드 (.env 파일 필수 - 디폴트 값 없음)
        self.api_key = api_key or os.getenv("VLLM_API_KEY")
        if not self.api_key:
            raise ValueError("VLLM_API_KEY 가 .env 파일에 설정되지 않았습니다.")

        self.base_url = base_url or os.getenv("VLLM_API_BASE")
        if not self.base_url:
            raise ValueError("VLLM_API_BASE 가 .env 파일에 설정되지 않았습니다.")

        self.model = model or os.getenv("VLLM_MODEL_NAME")
        if not self.model:
            raise ValueError("VLLM_MODEL_NAME 이 .env 파일에 설정되지 않았습니다.")

        # OpenAI 클라이언트 초기화
        # base_url: vLLM 서버 주소 (OpenAI API 엔드포인트)
        # api_key: vLLM API 키
        # timeout: 긴 응답을 위한 타임아웃 설정
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout=timeout, connect=10.0),
            max_retries=max_retries,
        )

        print(f"[LLMClient] 초기화 완료: {self.model}")
        print(f"[LLMClient] 연결: {self.base_url}")
        print("[LLMClient] .env 에서 설정을 로드했습니다.")

    def chat(
        self,
        messages: List[ChatCompletionMessageParam],
        temperature: float = 0.7,
        max_tokens: Optional[int] = 200,  # 기본값 200 으로 설정 (속도 개선)
        top_p: float = 0.9,
        stream: bool = False,
        **kwargs,
    ) -> Union[str, None]:
        """
        채팅 메시지 전송 및 응답 받기

        Chat Completions API 를 사용하여 대화 형식으로 LLM 에게 질문합니다.

        Args:
            messages: 대화 메시지 리스트 (시스템, 사용자, 어시스턴트 역할 포함)
                    예: [{"role": "system", "content": "당신은 NPC 입니다."},
                        {"role": "user", "content": "안녕하세요!"}]
            temperature: 응답 무작위성 (0.0~2.0, 높을수록 창의적)
            max_tokens: 최대 응답 토큰 수 (None 일 경우 모델 제한 사용)
            top_p: nucleus sampling 파라미터 (0.1~1.0)
            stream: 스트리밍 모드 (True 일 경우 None 반환, 콜백 사용)
            **kwargs: 추가 파라미터 (frequency_penalty, presence_penalty 등)

        Returns:
            str: LLM 의 응답 텍스트 (stream=False 일 경우)
            None: stream=True 일 경우 (스트리밍은 별도 처리)

        Example:
            >>> client = LLMClient()
            >>> response = client.chat([
            ...     {"role": "system", "content": "당신은 친절한 NPC 입니다."},
            ...     {"role": "user", "content": "안녕하세요?"}
            ... ])
            >>> print(response)
            "안녕하세요! 무엇을 도와드릴까요?"
        """
        # API 요청 파라미터 구성
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream,
            **kwargs,
        }

        # max_tokens 이 설정된 경우에만 추가
        if max_tokens is not None:
            params["max_tokens"] = max_tokens

        # API 요청
        response = self.client.chat.completions.create(**params)

        # 응답 추출
        if stream:
            return None  # 스트리밍은 별도 처리 필요

        return response.choices[0].message.content

    def chat_stream(
        self,
        messages: List[ChatCompletionMessageParam],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 0.9,
        **kwargs,
    ):
        """
        스트리밍 방식으로 채팅 응답 받기

        응답이 생성됨에 따라 실시간으로 토큰을 스트리밍합니다.

        Args:
            messages: 대화 메시지 리스트
            temperature: 응답 무작위성
            max_tokens: 최대 응답 토큰 수
            top_p: nucleus sampling 파라미터
            **kwargs: 추가 파라미터

        Yields:
            str: 생성된 토큰 (부분 문자열)

        Example:
            >>> client = LLMClient()
            >>> for chunk in client.chat_stream(messages):
            ...     print(chunk, end="", flush=True)
        """
        # API 요청 (스트리밍 모드)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=True,
            **kwargs,
        )

        # 스트리밍 응답 처리
        for chunk in response:
            # 각 chunk 에서 content 추출
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 0.9,
        **kwargs,
    ) -> str:
        """
        프롬프트 기반 텍스트 생성

        Chat API 를 사용하여 텍스트를 생성합니다. 시스템 프롬프트를 포함하여
        단일 사용자 입력으로 간주합니다.

        Args:
            prompt: 입력 프롬프트 (텍스트)
            temperature: 응답 무작위성
            max_tokens: 최대 응답 토큰 수
            top_p: nucleus sampling 파라미터
            **kwargs: 추가 파라미터

        Returns:
            str: 생성된 텍스트

        Example:
            >>> client = LLMClient()
            >>> response = client.generate("옛날 옛적에")
            >>> print(response)
            "...옛날 옛적에 산 작은 마을이 있었습니다..."
        """
        # 프롬프트를 채팅 형식으로 변환
        messages = [{"role": "user", "content": prompt}]

        result = self.chat(
            messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            **kwargs,
        )
        # result 는 chat() 의 반환 타입이 Union[str, None] 이지만, generate() 는 항상 str 을 반환해야 함
        # chat() 은 stream=False 일 때만 호출되므로 항상 str 을 반환함
        return result if result is not None else ""

    def get_model_info(self) -> Dict[str, Any]:
        """
        현재 연결된 모델 정보 가져오기

        Returns:
            dict: 모델 정보 (이름, 기본 설정 등)
        """
        return {
            "model": "****",  # 보안상 숨김
            "base_url": "****",  # 보안상 숨김
            "api_key_set": bool(self.api_key and self.api_key != "sk-xxx"),
        }


# 유틸리티 함수: 환경 변수 검증
def validate_env() -> bool:
    """
    필수 환경 변수가 설정되었는지 검증

    Returns:
        bool: 모든 환경 변수가 설정되면 True
    """
    required_vars = ["VLLM_API_BASE", "VLLM_API_KEY", "VLLM_MODEL_NAME"]
    missing = [var for var in required_vars if not os.getenv(var)]

    if missing:
        print(f"[ERROR] 다음 환경 변수가 .env 파일에 설정되지 않았습니다: {missing}")
        print("다음 명령어로 .env 파일을 확인하세요: cat .env")
        return False

    return True


# 예제 사용 코드
if __name__ == "__main__":
    # 클라이언트 초기화
    client = LLMClient()

    # 모델 정보 출력
    print("\n=== 모델 정보 ===")
    info = client.get_model_info()
    for key, value in info.items():
        print(f"{key}: {value}")

    # 간단한 채팅 테스트
    print("\n=== 채팅 테스트 ===")
    messages = [
        {
            "role": "system",
            "content": "당신은 NPC 입니다.",
        },
        {"role": "user", "content": "안녕하세요!"},
    ]

    response = client.chat(messages)
    print(f"NPC: {response}")
