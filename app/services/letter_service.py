# app/services/letter_service.py

from typing import List
from app.schemas.letter_schema import LetterCreate, LetterResponse


def create_letter(user_id: int | None, data: LetterCreate) -> LetterResponse:
    """
    편지 작성
    - 로그인 한 유저라면 user_id를 작성자로 기록할 수 있음
    - 익명도 가능하게 설계할 수 있음
    """
    # TODO: DB에 Letter 저장
    raise NotImplementedError


def list_letters_for_capsule(capsule_id: int, current_user_id: int | None) -> List[LetterResponse]:
    """
    특정 캡슐에 달린 편지 목록 조회
    - 캡슐이 열렸는지 / 권한이 있는지 체크할 수도 있음
    """
    # TODO: DB에서 capsule_id로 편지 리스트 조회
    raise NotImplementedError
