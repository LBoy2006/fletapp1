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


async def generate_agent_number(db: AsyncSession) -> str:
    """Return next agent number like chn_001, chn_002, ..."""
    result = await db.execute(select(models.User.agent_number))
    max_num = 0
    for agent in result.scalars().all():
        if agent and agent.startswith("chn_"):
            part = agent.split("_")[-1]
            if part.isdigit():
                max_num = max(max_num, int(part))
    return f"chn_{max_num + 1:03d}"


async def create_user(
    db: AsyncSession,
    *,
    user_id: int,
    agent_number: str,
    telegram_username: str | None = None,
    referrer_id: int | None = None,
) -> models.User:
    user = models.User(
        id=user_id,
        agent_number=agent_number,
        telegram_username=telegram_username,
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
    user = await get_user(db, user_id)
    join_date = user.join_date if user else date.today()
    stat = models.Affiliate(
        user_id=user_id,
        join_date=join_date,
        motivation=phrase,
        referral_link=link,
    )
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


async def list_categories(db: AsyncSession) -> list[str]:
    result = await db.execute(select(models.Supplier.categories))
    cats = result.scalars().all()
    unique = set()
    for c in cats:
        if c:
            unique.update(c)
    return sorted(unique)


async def list_suppliers(
    db: AsyncSession,
) -> list[models.Supplier]:
    result = await db.execute(select(models.Supplier))
    return result.scalars().all()


async def get_favorite_supplier_ids(db: AsyncSession, user_id: int) -> list[int]:
    result = await db.execute(
        select(models.FavoriteSupplier.supplier_id).where(models.FavoriteSupplier.user_id == user_id)
    )
    return [r for r in result.scalars().all()]


async def get_supplier_favorites_count(db: AsyncSession, supplier_id: int) -> int:
    result = await db.execute(
        select(func.count(models.FavoriteSupplier.id)).where(
            models.FavoriteSupplier.supplier_id == supplier_id
        )
    )
    return result.scalar_one()


async def get_all_favorites_count(db: AsyncSession) -> dict[int, int]:
    result = await db.execute(
        select(
            models.FavoriteSupplier.supplier_id,
            func.count(models.FavoriteSupplier.id)
        ).group_by(models.FavoriteSupplier.supplier_id)
    )
    return {sid: cnt for sid, cnt in result.all()}


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


async def get_favorite_find_ids(db: AsyncSession, user_id: int) -> list[int]:
    result = await db.execute(
        select(models.FavoriteFind.find_id).where(models.FavoriteFind.user_id == user_id)
    )
    return [r for r in result.scalars().all()]


async def toggle_favorite_find(db: AsyncSession, user_id: int, find_id: int) -> bool:
    result = await db.execute(
        select(models.FavoriteFind).where(
            models.FavoriteFind.user_id == user_id,
            models.FavoriteFind.find_id == find_id,
        )
    )
    fav = result.scalar_one_or_none()
    if fav:
        await db.delete(fav)
        await db.commit()
        return False
    else:
        fav = models.FavoriteFind(user_id=user_id, find_id=find_id)
        db.add(fav)
        await db.commit()
        return True


async def get_find_favorites_count(db: AsyncSession, find_id: int) -> int:
    result = await db.execute(
        select(func.count(models.FavoriteFind.id)).where(
            models.FavoriteFind.find_id == find_id
        )
    )
    return result.scalar_one()


async def get_all_find_favorites_count(db: AsyncSession) -> dict[int, int]:
    result = await db.execute(
        select(
            models.FavoriteFind.find_id,
            func.count(models.FavoriteFind.id)
        ).group_by(models.FavoriteFind.find_id)
    )
    return {fid: cnt for fid, cnt in result.all()}


async def get_supplier(db: AsyncSession, supplier_id: int) -> models.Supplier | None:
    result = await db.execute(select(models.Supplier).where(models.Supplier.id == supplier_id))
    return result.scalar_one_or_none()

async def list_find_categories(db: AsyncSession) -> list[str]:
    result = await db.execute(select(models.Find.category).distinct())
    cats = result.scalars().all()
    return [c for c in cats if c]


async def list_find_brands(db: AsyncSession, categories: list[str] | None = None) -> list[str]:
    stmt = select(models.Find.brand)
    if categories:
        stmt = stmt.where(models.Find.category.in_(categories))
    result = await db.execute(stmt.distinct())
    cats = result.scalars().all()
    return [c for c in cats if c]


async def list_finds(
    db: AsyncSession,
) -> list[models.Find]:
    stmt = select(models.Find).order_by(models.Find.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_payment(
    db: AsyncSession,
    *,
    user_id: int,
    months: int,
    amount: int,
    currency: str,
    invoice_id: str,
    status: str,
    payment_url: str,
) -> models.Payment:
    payment = models.Payment(
        user_id=user_id,
        months=months,
        amount=amount,
        currency=currency,
        invoice_id=invoice_id,
        status=status,
        payment_url=payment_url,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment
