from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.database.models.user import UserDB
from app.api.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
from app.models.application import ApplicationStatus, ApplicationType
from app.services.application_service import ApplicationService

router = APIRouter(
    prefix="/api/applications",
    tags=["Applications"],
)

@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application: ApplicationCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApplicationResponse:
    service = ApplicationService(db)

    try:
        return service.create_application(
            company_id=application.company_id,
            position=application.position,
            application_type=application.application_type.value,
            date_applied=application.date_applied,
            status=application.status.value,
            location=application.location,
            deadline=application.deadline,
            job_url=application.job_url,
            notes=application.notes,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[ApplicationResponse],
)
def get_applications(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: ApplicationStatus | None = Query(default=None),
    application_type: ApplicationType | None = Query(default=None),
    company_id: int | None = Query(default=None, gt=0),
    date_applied: date | None = None,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[ApplicationResponse]:
    service = ApplicationService(db)

    offset = (page - 1) * page_size

    return service.filter_applications(
        status=status.value if status is not None else None,
        application_type=(
            application_type.value
            if application_type is not None
            else None
        ),
        company_id=company_id,
        date_applied=date_applied,
        offset=offset,
        limit=page_size,
        user_id=current_user.id,
    )

@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application(
    application_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApplicationResponse:
    service = ApplicationService(db)

    application = service.get_application(
        application_id=application_id,
        user_id=current_user.id,
    )
    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    return application


@router.put(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application(
    application_id: int,
    application: ApplicationUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ApplicationResponse:
    service = ApplicationService(db)

    try:
        updated_application = service.update_application(
            application_id=application_id,
            user_id=current_user.id,
            position=application.position,
            application_type=(
                application.application_type.value
                if application.application_type is not None
                else None
            ),
            date_applied=application.date_applied,
            status=(
                application.status.value
                if application.status is not None
                else None
            ),
            location=application.location,
            deadline=application.deadline,
            job_url=application.job_url,
            notes=application.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if updated_application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    return updated_application


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_application(
    application_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    service = ApplicationService(db)

    deleted = service.delete_application(
        application_id=application_id,
        user_id=current_user.id,
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )