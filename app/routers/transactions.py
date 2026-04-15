from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.category import TransactionType
from app.models.tag import Tag
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["Transactions"])


def _base_query(user_id: int):
    return (
        select(Transaction)
        .options(selectinload(Transaction.category), selectinload(Transaction.tags))
        .where(Transaction.user_id == user_id)
    )


@router.get("/", response_model=list[TransactionRead])
async def list_transactions(
    type: TransactionType | None = Query(default=None),
    category_id: int | None = Query(default=None),
    tag_id: int | None = Query(default=None),
    date_from: str | None = Query(default=None),
    date_to: str | None = Query(default=None),
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = _base_query(current_user.id)

    if type:
        query = query.where(Transaction.type == type)
    if category_id:
        query = query.where(Transaction.category_id == category_id)
    if tag_id:
        query = query.where(Transaction.tags.any(Tag.id == tag_id))
    if date_from:
        query = query.where(Transaction.date >= date_from)
    if date_to:
        query = query.where(Transaction.date <= date_to)

    query = query.order_by(Transaction.date.desc(), Transaction.id.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if data.category_id:
        from app.models.category import Category
        cat = await db.execute(
            select(Category).where(
                Category.id == data.category_id,
                Category.user_id == current_user.id,
            )
        )
        if not cat.scalar_one_or_none():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    tags = []
    if data.tag_ids:
        result = await db.execute(
            select(Tag).where(Tag.id.in_(data.tag_ids), Tag.user_id == current_user.id)
        )
        tags = result.scalars().all()
        if len(tags) != len(data.tag_ids):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One or more tags not found")

    transaction = Transaction(
        amount=data.amount,
        type=data.type,
        description=data.description,
        date=data.date,
        category_id=data.category_id,
        user_id=current_user.id,
        tags=tags,
    )
    db.add(transaction)
    await db.flush()

    result = await db.execute(
        _base_query(current_user.id).where(Transaction.id == transaction.id)
    )
    return result.scalar_one()


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        _base_query(current_user.id).where(Transaction.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        _base_query(current_user.id).where(Transaction.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")

    update_data = data.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for field, value in update_data.items():
        setattr(transaction, field, value)

    if data.tag_ids is not None:
        tags_result = await db.execute(
            select(Tag).where(Tag.id.in_(data.tag_ids), Tag.user_id == current_user.id)
        )
        transaction.tags = tags_result.scalars().all()

    await db.flush()

    result = await db.execute(
        _base_query(current_user.id).where(Transaction.id == transaction_id)
    )
    return result.scalar_one()


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == current_user.id,
        )
    )
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    await db.delete(transaction)
