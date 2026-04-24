"""
LLM 스트리밍 테스트

스트리밍 모드로 응답을 실시간으로 받아 타임아웃 문제를 해결합니다.
"""

import sys
import time
from pathlib import Path

# 프로젝트 루트를 sys.path 에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.llm_client import LLMClient
from src.utils.time_utils import format_time


# 클라이언트 초기화
client = LLMClient()

# 스트리밍 테스트
print("\n=== 스트리밍 테스트 ===")
messages = [
    {"role": "system", "content": "당신은 NPC 입니다."},
    {"role": "user", "content": "안녕하세요?"}
]

print("NPC: ", end="", flush=True)
try:
    total_time = 0
    first_token_time = None
    token_count = 0
    
    start_time = time.time()
    for chunk in client.chat_stream(messages, temperature=0.7):
        chunk_start = time.time()
        print(chunk, end="", flush=True)
        
        if first_token_time is None:
            first_token_time = chunk_start - start_time
        total_time += time.time() - chunk_start
        token_count += 1
    
    total_elapsed = time.time() - start_time
    
    print("\n")
    print(f"\n=== 성능 측정 ===")
    if first_token_time:
        print(f"첫 토큰까지 시간: {format_time(first_token_time)}")
    print(f"전체 응답 시간: {format_time(total_elapsed)}")
    print(f"토큰 수: {token_count}")
    print(f"평균 토큰 처리 시간: {total_elapsed/token_count:.2f}초/토큰")
except Exception as e:
    print(f"\n에러: {e}")
