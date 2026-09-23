from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.database.models.user import UserDB
from app.api.schemas.follow_up import (
    FollowUpCreate,
    FollowUpResponse,
    FollowUpUpdate,
)
from app.models.follow_up import FollowUp
from app.services.follow_up_service import FollowUpService


router = APIRouter(
    prefix="/api/follow-ups",
    tags=["Follow-ups"],
)


@router.post(
    "",
    response_model=FollowUpResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_follow_up(
    follow_up: FollowUpCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FollowUpResponse:
    service = FollowUpService(db)

    follow_up_model = FollowUp(
        application_id=follow_up.application_id,
        follow_up_at=follow_up.follow_up_at,
        note=follow_up.note,
        completed=follow_up.completed,
    )

    try:
        return service.create_follow_up(
            follow_up=follow_up_model,
            user_id=current_user.id,
        )
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[FollowUpResponse],
)
def get_follow_ups(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> list[FollowUpResponse]:
    service = FollowUpService(db)

    offset = (page - 1) * page_size

    return service.get_follow_ups(
        offset=offset,
        limit=page_size,
        user_id=current_user.id,
    )


@router.get(
    "/{follow_up_id}",
    response_model=FollowUpResponse,
)
def get_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> FollowUpResponse:
    service = FollowUpService(db)
    follow_up = service.get_follow_up(
        follow_up_id=follow_up_id,
        user_id=current_user.id,
    )

    if follow_up is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow-up not found.",
        )

    return follow_up


@router.put(
    "/{follow_up_id}",
    response_model=FollowUpResponse,
)
def update_follow_up(
    follow_up_id: int,
    follow_up: FollowUpUpdate,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> FollowUpResponse:
    service = FollowUpService(db)

    if follow_up.completed:
        updated_follow_up = service.complete_follow_up(
            follow_up_id=follow_up_id,
            user_id=current_user.id,
        )
    else:
        updated_follow_up = service.reopen_follow_up(
            follow_up_id=follow_up_id,
            user_id=current_user.id,
        )
    if updated_follow_up is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow-up not found.",
        )

    return updated_follow_up


@router.delete(
    "/{follow_up_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
) -> None:
    service = FollowUpService(db)
    deleted = service.delete_follow_up(
        follow_up_id=follow_up_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow-up not found.",
        )
