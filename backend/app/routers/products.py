from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..schemas import PagedProducts, PageMeta, ProductOut
from ..crud.products import list_products

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=PagedProducts)
async def browse_products(
    category_id: int | None = Query(None),
    q: str | None = Query(None),
    sort: str | None = Query(None),
    min_price: int | None = Query(None, ge=0),
    max_price: int | None = Query(None, ge=0),
    page: int = Query(1, ge=1),
    page_size: int = Query(12, ge=1, le=48),
    db: AsyncSession = Depends(get_db),
):
    items, total = await list_products(db, category_id=category_id, q=q, sort=sort,
                                       min_price=min_price, max_price=max_price,
                                       page=page, page_size=page_size)
    data = [ProductOut.model_validate(i, from_attributes=True) for i in items]
    return {"data": data, "meta": PageMeta(page=page, page_size=page_size, total=total)}
