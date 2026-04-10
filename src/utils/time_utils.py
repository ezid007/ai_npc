"""
시간 유틸리티 모듈

모든 시간 관련 포맷팅 및 계산 기능을 제공합니다.
"""

from typing import Optional


def format_time(seconds: float) -> str:
    """
    초를 시:분:초 형식으로 변환
    
    Args:
        seconds: 초 단위 시간
        
    Returns:
        포맷팅된 시간 문자열 (예: "2 분 51 초", "3.24 초")
    """
    if seconds is None:
        return "N/A"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}시간 {minutes}분 {secs:.2f}초"
    elif minutes > 0:
        return f"{minutes}분 {secs:.2f}초"
    else:
        return f"{secs:.2f}초"


def format_time_detailed(seconds: float) -> str:
    """
    초를 상세한 형식으로 변환 (시:분:초)
    
    Args:
        seconds: 초 단위 시간
        
    Returns:
        포맷팅된 시간 문자열 (예: "00:02:51")
    """
    if seconds is None:
        return "N/A"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_duration(start_time: float, end_time: Optional[float] = None) -> str:
    """
    시작 시간과 종료 시간 사이의 차이를 포맷팅
    
    Args:
        start_time: 시작 시간 (time.time() 결과)
        end_time: 종료 시간 (없으면 현재 시간 사용)
        
    Returns:
        포맷팅된 시간 문자열
    """
    import time
    if end_time is None:
        end_time = time.time()
    
    duration = end_time - start_time
    return format_time(duration)


def calculate_tokens_per_second(token_count: int, total_time: float) -> float:
    """
    초당 토큰 수 계산
    
    Args:
        token_count: 토큰 개수
        total_time: 총 시간 (초)
        
    Returns:
        초당 토큰 수
    """
    if total_time <= 0 or token_count <= 0:
        return 0.0
    return token_count / total_time


def format_tokens_per_second(token_count: int, total_time: float) -> str:
    """
    초당 토큰 수를 포맷팅된 문자열로 반환
    
    Args:
        token_count: 토큰 개수
        total_time: 총 시간 (초)
        
    Returns:
        포맷팅된 토큰/초 문자열
    """
    tps = calculate_tokens_per_second(token_count, total_time)
    return f"{tps:.2f} 토큰/초"


# 예제 사용
if __name__ == "__main__":
    # 테스트
    print(f"171.20 초 = {format_time(171.20)}")
    print(f"174.82 초 = {format_time(174.82)}")
    print(f"3.24 초 = {format_time(3.24)}")
    print(f"171.20 초 (상세) = {format_time_detailed(171.20)}")
