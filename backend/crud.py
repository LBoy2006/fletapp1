from __future__ import annotations

import base64
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from . import models


def encode_referral(user_id: int) -> str:
    """Encode user id for referral link."""
    return base64.urlsafe_b64encode(str(user_id).encode()).decode()


def decode_referral(code: str) -> int:
    """Decode user id from referral code."""
    return int(base64.urlsafe_b64decode(code.encode()).decode())


def generate_referral_link(user_id: int) -> str:
    code = encode_referral(user_id)
    return f"https://t.me/club_bot?start={code}"


async def create_user(
    db: AsyncSession,
    *,
    user_id: int,
    agent_number: str,
    referrer_id: int | None = None,
) -> models.User:
    user = models.User(
        id=user_id,
        agent_number=agent_number,
        join_date=date.today(),
        location="",
        is_member=False,
        referrer_id=referrer_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_affiliate(db: AsyncSession, user_id: int) -> models.Affiliate:
    result = await db.execute(
        select(models.MotivationPhrase.text).order_by(func.random()).limit(1)
    )
    phrase = result.scalar_one_or_none() or ""
    link = generate_referral_link(user_id)
    stat = models.Affiliate(user_id=user_id, motivation=phrase, referral_link=link)
    db.add(stat)
    await db.commit()
    await db.refresh(stat)
    return stat


async def get_user(db: AsyncSession, user_id: int) -> models.User | None:
    """Return user by id or None."""
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()


async def update_user(db: AsyncSession, user_id: int, *, location: str | None = None) -> models.User | None:
    """Update user fields and return updated instance or None if not found."""
    user = await get_user(db, user_id)
    if not user:
        return None
    if location is not None:
        user.location = location
    await db.commit()
    await db.refresh(user)
    return user


async def set_membership(db: AsyncSession, user_id: int, value: bool) -> models.User | None:
    """Set user's membership status."""
    user = await get_user(db, user_id)
    if not user:
        return None
    user.is_member = value
    await db.commit()
    await db.refresh(user)
    return user


async def get_affiliate(db: AsyncSession, user_id: int) -> models.Affiliate | None:
    result = await db.execute(select(models.Affiliate).where(models.Affiliate.user_id == user_id))
    return result.scalar_one_or_none()


async def request_withdraw(db: AsyncSession, user_id: int) -> models.Affiliate | None:
    stat = await get_affiliate(db, user_id)
    if not stat:
        return None
    stat.withdraw_requested = True
    await db.commit()
    await db.refresh(stat)
    return stat


async def list_categories1(db: AsyncSession) -> list[str]:
    result = await db.execute(select(models.Supplier.category1).distinct())
    cats = result.scalars().all()
    return [c for c in cats if c]


async def list_categories2(db: AsyncSession, categories1: list[str] | None = None) -> list[str]:
    stmt = select(models.Supplier.category2)
    if categories1:
        stmt = stmt.where(models.Supplier.category1.in_(categories1))
    result = await db.execute(stmt.distinct())
    cats = result.scalars().all()
    return [c for c in cats if c]


async def list_suppliers(
    db: AsyncSession,
    categories1: list[str] | None = None,
    categories2: list[str] | None = None,
) -> list[models.Supplier]:
    stmt = select(models.Supplier)
    if categories1:
        stmt = stmt.where(models.Supplier.category1.in_(categories1))
    if categories2:
        stmt = stmt.where(models.Supplier.category2.in_(categories2))
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_favorite_supplier_ids(db: AsyncSession, user_id: int) -> list[int]:
    result = await db.execute(
        select(models.FavoriteSupplier.supplier_id).where(models.FavoriteSupplier.user_id == user_id)
    )
    return [r for r in result.scalars().all()]


async def toggle_favorite_supplier(db: AsyncSession, user_id: int, supplier_id: int) -> bool:
    result = await db.execute(
        select(models.FavoriteSupplier).where(
            models.FavoriteSupplier.user_id == user_id,
            models.FavoriteSupplier.supplier_id == supplier_id,
        )
    )
    fav = result.scalar_one_or_none()
    if fav:
        await db.delete(fav)
        await db.commit()
        return False
    else:
        fav = models.FavoriteSupplier(user_id=user_id, supplier_id=supplier_id)
        db.add(fav)
        await db.commit()
        return True


async def get_supplier(db: AsyncSession, supplier_id: int) -> models.Supplier | None:
    result = await db.execute(select(models.Supplier).where(models.Supplier.id == supplier_id))
    return result.scalar_one_or_none()


async def list_finds(db: AsyncSession) -> list[models.Find]:
    result = await db.execute(select(models.Find).order_by(models.Find.created_at.desc()))
    return result.scalars().all()
