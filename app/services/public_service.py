# app/services/public_service.py

from typing import List

from app.schemas.public_schema import PublicCapsuleResponse


def list_public_capsules() -> List[PublicCapsuleResponse]:
    """
    공개 캡슐 목록 조회
    - is_public=True 인 것만
    - 정렬 기준: 최근 생성순 / 열리는 날짜순 등
    """
    # TODO: DB에서 is_public=True 조건으로 조회
    raise NotImplementedError


def get_public_capsule_detail(capsule_id: int) -> PublicCapsuleResponse:
    """
    공개 캡슐 상세 조회
    """
    # TODO: 공개 캡슐 단일 조회
    raise NotImplementedError
