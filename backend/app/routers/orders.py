from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..schemas import CheckoutGuestIn, OrderOut, OrdersPage, PageMeta
from ..crud.orders import create_guest_order, list_orders, get_order_by_code

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/checkout/guest", response_model=OrderOut)
async def checkout_guest(payload: CheckoutGuestIn, db: AsyncSession = Depends(get_db)):
    try:
        order = await create_guest_order(db, email=payload.email, name=payload.name,
                                         items=[i.model_dump() for i in payload.items])
        return OrderOut(
            id=order.id,
            order_code=order.order_code,
            status=order.status.value,
            total_cents=order.total_cents,
            created_at=str(order.created_at),
            items=[{
                "product_id": it.product_id,
                "name": it.product.name,
                "qty": it.qty,
                "price_cents": it.price_cents
            } for it in order.items]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=OrdersPage)
async def list_orders_route(
    email: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    rows, total = await list_orders(db, email=email, page=page, page_size=page_size)
    data = [OrderOut(
        id=o.id,
        order_code=o.order_code,
        status=o.status.value,
        total_cents=o.total_cents,
        created_at=str(o.created_at),
        items=[{
            "product_id": it.product_id,
            "name": it.product.name,
            "qty": it.qty,
            "price_cents": it.price_cents
        } for it in o.items]
    ) for o in rows]
    return {"data": data, "meta": PageMeta(page=page, page_size=page_size, total=total)}

@router.get("/{order_code}", response_model=OrderOut)
async def get_order_detail(order_code: str, db: AsyncSession = Depends(get_db)):
    o = await get_order_by_code(db, order_code)
    if not o:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderOut(
        id=o.id,
        order_code=o.order_code,
        status=o.status.value,
        total_cents=o.total_cents,
        created_at=str(o.created_at),
        items=[{
            "product_id": it.product_id,
            "name": it.product.name,
            "qty": it.qty,
            "price_cents": it.price_cents
        } for it in o.items]
    )
