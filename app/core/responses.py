# app/core/responses.py
from typing import Generic, List, Optional, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class CommonResponse(GenericModel, Generic[T]):
    """
    모든 API가 공통으로 사용하는 응답 래퍼
    """

    code: int = 0  # 0 == success, 그 외는 에러 코드
    message: str = "success"
    data: Optional[T] = None  # 실제 응답 데이터
    meta: Optional[dict] = None  # 부가 정보 (검증 에러, 페이징 정보 등)


class PagingResult(GenericModel, Generic[T]):
    """
    페이징이 필요한 API에서 data에 들어가는 형태
    """

    items: List[T]
    total: int
    page: int
    size: int
