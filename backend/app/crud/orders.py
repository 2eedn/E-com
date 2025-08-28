from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Order, OrderItem, Product
from typing import List, Tuple
import secrets

async def create_guest_order(db: AsyncSession, *, email: str, name: str, items: List[dict]) -> Order:
    product_ids = [i["product_id"] for i in items]
    products = (await db.execute(select(Product).where(Product.id.in_(product_ids)))).scalars().all()
    pmap = {p.id: p for p in products}
    total = 0
    order = Order(order_code=secrets.token_hex(6).upper(), guest_email=email, guest_name=name, total_cents=0)
    for it in items:
        p = pmap.get(it["product_id"])
        if not p:
            raise ValueError(f"Product {it['product_id']} not found")
        qty = int(it["qty"])
        if qty <= 0:
            raise ValueError("qty must be > 0")
        total += p.price_cents * qty
        order.items.append(OrderItem(product_id=p.id, qty=qty, price_cents=p.price_cents))
    order.total_cents = total
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order

async def list_orders(db: AsyncSession, *, email: str = None, page: int = 1, page_size: int = 10) -> Tuple[List[Order], int]:
    stmt = select(Order).order_by(Order.id.desc())
    if email:
        stmt = stmt.where(Order.guest_email == email)
    from sqlalchemy import func
    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()
    rows = (await db.execute(stmt.limit(page_size).offset((page-1)*page_size))).scalars().unique().all()
    return rows, total

async def get_order_by_code(db: AsyncSession, code: str):
    return (await db.execute(select(Order).where(Order.order_code == code))).scalars().first()
