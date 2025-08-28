from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum

class OrderStatus(str, Enum):
    NEW = "NEW"
    PAID = "PAID"
    CANCELLED = "CANCELLED"
    FULFILLED = "FULFILLED"

class CategoryOut(BaseModel):
    id: int
    name: str

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price_cents: int
    image_url: Optional[str]
    category: Optional[CategoryOut]

class ProductFilter(BaseModel):
    category_id: Optional[int] = None
    q: Optional[str] = None
    sort: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    page: int = 1
    page_size: int = 12

class PageMeta(BaseModel):
    page: int
    page_size: int
    total: int

class PagedProducts(BaseModel):
    data: List[ProductOut]
    meta: PageMeta

class CartItem(BaseModel):
    product_id: int
    qty: int = Field(gt=0)

class CheckoutGuestIn(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1)
    items: List[CartItem]

class OrderItemOut(BaseModel):
    product_id: int
    name: str
    qty: int
    price_cents: int

class OrderOut(BaseModel):
    id: int
    order_code: str
    status: OrderStatus
    total_cents: int
    created_at: str
    items: List[OrderItemOut]
