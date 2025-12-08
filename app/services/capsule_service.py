# app/services/capsule_service.py

from typing import List

from app.schemas.capsule_schema import CapsuleCreate, CapsuleResponse, CapsuleUpdate


def create_capsule(user_id: int, data: CapsuleCreate) -> CapsuleResponse:
    """
    타임캡슐 생성 로직
    - user_id 주인으로 캡슐 생성
    - DB에 저장 후 CapsuleResponse 반환
    """
    # TODO: DB 모델과 연결해서 구현
    raise NotImplementedError


def get_capsule_detail(
    capsule_id: int, current_user_id: int | None = None
) -> CapsuleResponse:
    """
    캡슐 상세 조회
    - 비공개 + 본인 아님이면 접근 불가
    - 열람 가능 시간인지 체크
    """
    # TODO:
    # - DB에서 capsule 조회
    # - is_capsule_open 사용
    # - 권한 체크
    raise NotImplementedError


def list_my_capsules(user_id: int) -> List[CapsuleResponse]:
    """
    내가 만든 캡슐 목록 조회
    """
    # TODO: DB에서 user_id로 필터해서 캡슐 리스트 조회
    raise NotImplementedError


def update_capsule(
    capsule_id: int, user_id: int, data: CapsuleUpdate
) -> CapsuleResponse:
    """
    캡슐 수정
    - 본인 소유 여부 확인
    - 필요한 필드만 업데이트
    """
    # TODO: DB update 로직
    raise NotImplementedError


def delete_capsule(capsule_id: int, user_id: int) -> None:
    """
    캡슐 삭제
    - 본인 소유 여부 확인 후 삭제
    """
    # TODO: DB delete 로직
    raise NotImplementedError
