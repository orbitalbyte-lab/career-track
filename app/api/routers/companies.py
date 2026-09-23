from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.database.models.user import UserDB
from app.api.schemas.company import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
)
from app.services.company_service import CompanyService


router = APIRouter(
    prefix="/api/companies",
    tags=["Companies"],
)


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    company: CompanyCreate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CompanyResponse:
    service = CompanyService(db)

    try:
        return service.create_company(
            user_id=current_user.id,
            name=company.name,
            website=company.website,
            industry=company.industry,
            location=company.location,
            notes=company.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[CompanyResponse],
)
def get_companies(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[CompanyResponse]:
    service = CompanyService(db)

    offset = (page - 1) * page_size

    return service.get_companies(
        offset=offset,
        limit=page_size,
        user_id=current_user.id,
    )

@router.get(
    "/{company_id}",
    response_model=CompanyResponse,
)
def get_company(
    company_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CompanyResponse:
    service = CompanyService(db)
    company = service.get_company(
        company_id=company_id,
        user_id=current_user.id,
    )

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found.",
        )

    return company


@router.put(
    "/{company_id}",
    response_model=CompanyResponse,
)
def update_company(
    company_id: int,
    company: CompanyUpdate,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CompanyResponse:
    service = CompanyService(db)

    try:
        updated_company = service.update_company(
            company_id=company_id,
            user_id=current_user.id,
            name=company.name,
            website=company.website,
            industry=company.industry,
            location=company.location,
            notes=company.notes,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if updated_company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found.",
        )

    return updated_company


@router.delete(
    "/{company_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_company(
    company_id: int,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    service = CompanyService(db)

    try:
        deleted = service.delete_company(
            company_id=company_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found.",
        )