# app/services/rollingpaper_service.py

from typing import List

from app.schemas.rollingpaper_schema import (
    RollingPaperCreate,
    RollingPaperResponse,
    RollingPaperUpdate,
)


def create_rollingpaper(user_id: int, data: RollingPaperCreate) -> RollingPaperResponse:
    """
    롤링페이퍼 생성 로직
    - user_id를 오너로 롤링페이퍼 생성
    - DB에 저장 후 RollingPaperResponse 반환
    """
    # TODO: DB 모델과 연결해서 구현
    raise NotImplementedError


def get_rollingpaper_detail(
    rollingpaper_id: int, current_user_id: int | None = None
) -> RollingPaperResponse:
    """
    롤링페이퍼 상세 조회
    - 비공개 + 본인 아님이면 접근 불가
    - 열람 가능 시간인지 체크
    """
    # TODO:
    # - DB에서 rollingpaper 조회
    # - 권한 체크
    raise NotImplementedError


def list_my_rollingpapers(user_id: int) -> List[RollingPaperResponse]:
    """
    내가 만든 롤링페이퍼 목록 조회
    """
    # TODO: DB에서 user_id로 필터해서 롤링페이퍼 리스트 조회
    raise NotImplementedError


def update_rollingpaper(
    rollingpaper_id: int, user_id: int, data: RollingPaperUpdate
) -> RollingPaperResponse:
    """
    롤링페이퍼 수정
    - 본인 소유 여부 확인
    - 필요한 필드만 업데이트
    """
    # TODO: DB update 로직
    raise NotImplementedError


def delete_rollingpaper(rollingpaper_id: int, user_id: int) -> None:
    """
    롤링페이퍼 삭제
    - 본인 소유 여부 확인 후 삭제
    """
    # TODO: DB delete 로직
    raise NotImplementedError
