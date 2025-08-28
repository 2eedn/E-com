from sqlalchemy import select, desc, asc, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Tuple, List
from ..models import Product, Category

async def list_products(db: AsyncSession, *,
                       category_id=None, q=None, sort=None,
                       min_price=None, max_price=None,
                       page: int = 1, page_size: int = 12) -> Tuple[List[Product], int]:
    stmt = select(Product).join(Category, isouter=True)
    if category_id:
        stmt = stmt.where(Product.category_id == category_id)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(Product.name.like(like))
    if min_price is not None:
        stmt = stmt.where(Product.price_cents >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price_cents <= max_price)
    if sort == "price_asc":
        stmt = stmt.order_by(asc(Product.price_cents))
    elif sort == "price_desc":
        stmt = stmt.order_by(desc(Product.price_cents))
    else:
        stmt = stmt.order_by(desc(Product.id))

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    offset = (page - 1) * page_size
    rows = (await db.execute(stmt.limit(page_size).offset(offset))).scalars().all()
    return rows, total
