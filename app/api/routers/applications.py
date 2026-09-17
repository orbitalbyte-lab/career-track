from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationUpdate,
)
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
    db: Session = Depends(get_db),
) -> list[ApplicationResponse]:
    service = ApplicationService(db)

    offset = (page - 1) * page_size

    return service.get_applications(
        offset=offset,
        limit=page_size,
    )

@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
) -> ApplicationResponse:
    service = ApplicationService(db)

    application = service.get_application(application_id)

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
    db: Session = Depends(get_db),
) -> ApplicationResponse:
    service = ApplicationService(db)

    try:
        updated_application = service.update_application(
            application_id=application_id,
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
    db: Session = Depends(get_db),
) -> None:
    service = ApplicationService(db)

    deleted = service.delete_application(application_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )