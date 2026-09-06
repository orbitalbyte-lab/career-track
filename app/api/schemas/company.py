from pydantic import BaseModel, ConfigDict


class CompanyBase(BaseModel):
    name: str
    website: str | None = None
    industry: str | None = None
    location: str | None = None
    notes: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    website: str | None = None
    industry: str | None = None
    location: str | None = None
    notes: str | None = None


class CompanyResponse(CompanyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int