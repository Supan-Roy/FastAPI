from datetime import datetime
from typing import Annotated, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, AnyUrl


class Dimensions(BaseModel):
    length: float = Field(..., ge=0)
    width: float = Field(..., ge=0)
    height: float = Field(..., ge=0)


class Seller(BaseModel):
    seller_id: UUID
    name: str
    email: Optional[str] = None
    website: Optional[str] = None


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
    name: str
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
    seller: Optional[Seller] = None
    created_at: Optional[datetime] = None
