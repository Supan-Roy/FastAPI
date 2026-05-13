from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID
from pydantic import (
    BaseModel,
    Field,
    AnyUrl,
    field_validator,
    model_validator,
    computed_field,
    EmailStr,
)


class Dimensions(BaseModel):
    length: float = Field(..., ge=0)
    width: float = Field(..., ge=0)
    height: float = Field(..., ge=0)

class Seller(BaseModel):
    id: UUID
    name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=50,
            title="Seller Name",
            description="Name of the Seller (2-50 chars).",
            examples=["Supan Roy", "Jonathan Byers", "Jupiter Sonic Labs Pvt Ltd."],
        ),
    ]
    email: EmailStr
    website: AnyUrl

    @field_validator("email", mode="after")
    @classmethod
    def validate_seller_email_domain(cls, value: EmailStr):
        allowed_domains = ["supanroy.com", "mistore.com", "mistore.in", "apple.com", "amazon.com", "amazon.in", "darazmall.com", "example.com"]
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"Seller email domain not allowed: {domain}")

        return value

class Product(BaseModel):
    id: UUID
    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=30,
            title="SKU",
            description="Stock Keeping Unit",
            examples=["734-gxc-676-4h", "rfy6-6700-p342"],
        ),
    ]
    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="Product Name",
            description="Readable product name (3-80 chars).",
            examples=["Xiaomi Model Pro", "Apple Model X"],
        ),
    ]
    description: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    price: float = Field(..., ge=0)
    currency: str = Field(..., min_length=1, max_length=4)
    discount_percent: int = Field(0, ge=0, le=100)
    stock: int = Field(0, ge=0)
    is_active: bool = True
    rating: Optional[float] = Field(None, ge=0, le=5)
    tags: Optional[List[str]] = None
    image_urls: Optional[List[AnyUrl]] = None
    dimensions_cm: Optional[Dimensions] = None
    seller: Seller
    created_at: datetime

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value: str):
        if "-" not in value:
            raise ValueError("SKU must have '-'")

        last = value.split("-")[-1]
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with a 3-digit sequence like -245")

        return value
    
    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model: "Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock is 0, is_active must be false")
        
        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted product must have a rating more than zero")
        
        return model

    @computed_field
    @property
    def final_price(self) -> float:
        return round(self.price * (1-self.discount_percent/100), 2)
    
    @computed_field
    @property
    def volume_cm3(self) -> float:
        d = self.dimensions_cm
        return round(d.length * d.width * d.height, 2)