"""
AI NPC 프로젝트 - 기본 대화 시스템

이 모듈은 vLLM API 를 활용한 기본 대화 시스템을 구현합니다.
NPC 페르소나를 설정하고 사용자와 대화할 수 있는 기능을 제공합니다.

학습 포인트:
- LLMClient 를 사용한 API 호출
- 시스템 프롬프트로 페르소나 설정
- 다중턴 대화 컨텍스트 유지
- 스트리밍 응답 처리
"""

import os
from typing import List, Dict, Any, Optional
from src.llm_client import LLMClient


class NPCConversation:
    """
    NPC 대화 관리 클래스

    사용자와 NPC 간의 대화를 관리하고, 페르소나를 유지하며 응답을 생성합니다.

    Attributes:
        client (LLMClient): LLM API 클라이언트
        persona (str): NPC 의 페르소나 (시스템 프롬프트)
        history (List[Dict]): 대화 히스토리
    """

    def __init__(self, client: LLMClient, persona: str = "당신은 친절한 NPC 입니다."):
        """
        NPCConversation 초기화

        Args:
            client: LLMClient 인스턴스
            persona: NPC 의 페르소나/성격을 정의하는 시스템 프롬프트
        """
        self.client = client
        self.persona = persona
        self.history: List[Dict[str, str]] = []

        print(f"[NPCConversation] 초기화 완료: 페르소나 = '{persona}'")

    def set_persona(self, persona: str) -> None:
        """
        NPC 페르소나 변경

        Args:
            persona: 새로운 페르소나 (시스템 프롬프트)
        """
        self.persona = persona
        # 히스토리 초기화 (새 페르소나 적용)
        self.history = []
        print(f"[NPCConversation] 페르소나 변경: '{persona}'")

    def get_context(self) -> List[Dict[str, str]]:
        """
        현재 대화 컨텍스트 (히스토리) 가져오기

        Returns:
            List[Dict]: 시스템 메시지와 대화 히스토리를 포함한 메시지 리스트
        """
        # 시스템 메시지로 시작
        context = [{"role": "system", "content": self.persona}]
        # 기존 히스토리 추가
        context.extend(self.history)
        return context

    def chat(self, user_message: str, **kwargs) -> str:
        """
        사용자의 메시지에 대한 응답 생성

        Args:
            user_message: 사용자의 입력 메시지
            **kwargs: LLMClient.chat() 에 전달할 추가 파라미터
                     (temperature, max_tokens 등)

        Returns:
            str: NPC 의 응답 메시지

        Example:
            >>> npc = NPCConversation(client, "당신은 판타지 세계의 상인입니다.")
            >>> response = npc.chat("안녕하세요! 무엇을 파나요?")
            >>> print(response)
            "안녕하세요! 귀여운 여행자님. 저는 이곳에서 다양한 물약과 장비를 판매합니다."
        """
        # 컨텍스트 구성
        context = self.get_context()

        # 사용자 메시지 추가
        context.append({"role": "user", "content": user_message})

        # LLM 에게 응답 요청
        response = self.client.chat(context, **kwargs)

        # 히스토리 업데이트
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": response})

        return response

    def chat_stream(self, user_message: str, **kwargs):
        """
        스트리밍 방식으로 응답 생성

        Args:
            user_message: 사용자의 입력 메시지
            **kwargs: LLMClient.chat_stream() 에 전달할 추가 파라미터

        Yields:
            str: 생성된 토큰 (실시간 응답)

        Example:
            >>> npc = NPCConversation(client, "당신은 친절한 NPC 입니다.")
            >>> for chunk in npc.chat_stream("안녕하세요!"):
            ...     print(chunk, end="", flush=True)
        """
        # 컨텍스트 구성
        context = self.get_context()
        context.append({"role": "user", "content": user_message})

        # 스트리밍 응답 받기
        response = ""
        for chunk in self.client.chat_stream(context, **kwargs):
            response += chunk
            yield chunk

        # 히스토리 업데이트 (스트리밍 완료 후)
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": response})

    def get_history(self) -> List[Dict[str, str]]:
        """
        전체 대화 히스토리 가져오기

        Returns:
            List[Dict]: 대화 히스토리 (시스템 메시지 포함)
        """
        return self.get_context()

    def clear_history(self) -> None:
        """대화 히스토리 초기화"""
        self.history = []
        print("[NPCConversation] 대화 히스토리 초기화")

    def get_summary(self) -> Dict[str, Any]:
        """
        대화 상태 요약

        Returns:
            dict: 대화 상태 정보
        """
        return {
            "persona": self.persona,
            "turn_count": len(self.history) // 2,  # user + assistant = 2
            "last_user_message": self.history[-1]["content"] if self.history else None,
            "last_assistant_message": (
                self.history[-2]["content"] if len(self.history) > 1 else None
            ),
        }


# 예제 사용 코드
if __name__ == "__main__":
    # LLM 클라이언트 초기화
    client = LLMClient()

    # NPC 페르소나 설정 (사용자가 .env 또는 코드에서 설정)
    persona = "당신은 NPC 입니다."

    # NPC 대화 세션 시작
    npc = NPCConversation(client, persona)

    print("\n=== AI NPC 대화 데모 ===")
    print(f"NPC: {persona}")
    print("입력: 'quit' 또는 'exit'로 종료\n")

    # 대화 루프
    while True:
        user_input = input("사용자: ").strip()

        if user_input.lower() in ["quit", "exit", "종료", "나가기"]:
            print("\n[AI NPC] 감사합니다!")
            break

        if not user_input:
            continue

        # NPC 응답 (스트리밍)
        print("NPC: ", end="", flush=True)
        try:
            for chunk in npc.chat_stream(user_input, temperature=0.8):
                print(chunk, end="", flush=True)
            print()  # 줄바꿈
        except Exception as e:
            print(f"\n[에러] 응답 생성 중 오류 발생: {e}")

        # 대화 요약 출력
        summary = npc.get_summary()
        print(f"[상태] 대화 턴: {summary['turn_count']}")
