from __future__ import annotations

from sqlalchemy.orm import Session

from . import models


def get_user(db: Session, user_id: int) -> models.User | None:
    """Return user by id or None."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: int, *, location: str | None = None) -> models.User | None:
    """Update user fields and return updated instance or None if not found."""
    user = get_user(db, user_id)
    if not user:
        return None
    if location is not None:
        user.location = location
    db.commit()
    db.refresh(user)
    return user


def set_membership(db: Session, user_id: int, value: bool) -> models.User | None:
    """Set user's membership status."""
    user = get_user(db, user_id)
    if not user:
        return None
    user.is_member = value
    db.commit()
    db.refresh(user)
    return user


def get_affiliate(db: Session, user_id: int) -> models.Affiliate | None:
    return db.query(models.Affiliate).filter(models.Affiliate.user_id == user_id).first()


def request_withdraw(db: Session, user_id: int) -> models.Affiliate | None:
    stat = get_affiliate(db, user_id)
    if not stat:
        return None
    stat.withdraw_requested = True
    db.commit()
    db.refresh(stat)
    return stat


def list_categories1(db: Session) -> list[str]:
    cats = db.query(models.Supplier.category1).distinct().all()
    return [c[0] for c in cats if c[0]]


def list_categories2(db: Session, categories1: list[str] | None = None) -> list[str]:
    q = db.query(models.Supplier.category2)
    if categories1:
        q = q.filter(models.Supplier.category1.in_(categories1))
    cats = q.distinct().all()
    return [c[0] for c in cats if c[0]]


def list_suppliers(
    db: Session,
    categories1: list[str] | None = None,
    categories2: list[str] | None = None,
) -> list[models.Supplier]:
    q = db.query(models.Supplier)
    if categories1:
        q = q.filter(models.Supplier.category1.in_(categories1))
    if categories2:
        q = q.filter(models.Supplier.category2.in_(categories2))
    return q.all()


def get_favorite_supplier_ids(db: Session, user_id: int) -> list[int]:
    return [
        r.supplier_id
        for r in db.query(models.FavoriteSupplier).filter(models.FavoriteSupplier.user_id == user_id)
    ]


def toggle_favorite_supplier(db: Session, user_id: int, supplier_id: int) -> bool:
    fav = db.query(models.FavoriteSupplier).filter(
        models.FavoriteSupplier.user_id == user_id,
        models.FavoriteSupplier.supplier_id == supplier_id,
    ).first()
    if fav:
        db.delete(fav)
        db.commit()
        return False
    else:
        fav = models.FavoriteSupplier(user_id=user_id, supplier_id=supplier_id)
        db.add(fav)
        db.commit()
        return True


def get_supplier(db: Session, supplier_id: int) -> models.Supplier | None:
    return db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()


def list_finds(db: Session) -> list[models.Find]:
    return db.query(models.Find).order_by(models.Find.created_at.desc()).all()
