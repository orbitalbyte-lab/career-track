from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
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

    return service.create_interview(interview_model)


@router.get(
    "",
    response_model=list[InterviewResponse],
)
def get_interviews(
    db: Session = Depends(get_db),
) -> list[InterviewResponse]:
    service = InterviewService(db)

    return service.get_interviews()


@router.get(
    "/{interview_id}",
    response_model=InterviewResponse,
)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
) -> InterviewResponse:
    service = InterviewService(db)

    interview = service.get_interview(interview_id)

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
) -> InterviewResponse:
    service = InterviewService(db)

    updated_interview = service.update_interview(
        interview_id=interview_id,
        status=interview.status.value,
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
) -> None:
    service = InterviewService(db)

    deleted = service.delete_interview(interview_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found.",
        )