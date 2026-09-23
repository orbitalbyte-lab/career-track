from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.database.models.user import UserDB
from app.api.schemas.interview import (
    InterviewCreate,
    InterviewResponse,
    InterviewUpdate,
)
from app.models.interview import Interview
from app.services.interview_service import InterviewService


router = APIRouter(
    prefix="/api/interviews",
    tags=["Interviews"],
)

@router.post(
    "",
    response_model=InterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview(
    interview: InterviewCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InterviewResponse:
    service = InterviewService(db)

    interview_model = Interview(
        application_id=interview.application_id,
        scheduled_at=interview.scheduled_at,
        interview_type=interview.interview_type,
        status=interview.status,
        outcome=interview.outcome,
        notes=interview.notes,
    )

    try:
        return service.create_interview(
            interview=interview_model,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[InterviewResponse],
)
def get_interviews(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> list[InterviewResponse]:
    service = InterviewService(db)

    offset = (page - 1) * page_size

    return service.get_interviews(
        offset=offset,
        limit=page_size,
        user_id=current_user.id,
    )


@router.get(
    "/{interview_id}",
    response_model=InterviewResponse,
)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> InterviewResponse:
    service = InterviewService(db)

    interview = service.get_interview(
        interview_id=interview_id,
        user_id=current_user.id,
    )

    if interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found.",
        )

    return interview


@router.put(
    "/{interview_id}",
    response_model=InterviewResponse,
)
def update_interview(
    interview_id: int,
    interview: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> InterviewResponse:
    service = InterviewService(db)

    updated_interview = service.update_interview(
        interview_id=interview_id,
        status=interview.status.value,
        user_id=current_user.id,
        outcome=(
            interview.outcome.value
            if interview.outcome is not None
            else None
        ),
    )

    if updated_interview is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found.",
        )

    return updated_interview


@router.delete(
    "/{interview_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> None:
    service = InterviewService(db)

    deleted = service.delete_interview(
        interview_id=interview_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found.",
        )