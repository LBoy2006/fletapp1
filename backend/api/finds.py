from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()


@router.get('/finds', response_model=list[schemas.FindOut])
async def list_finds(db: AsyncSession = Depends(get_db)):
    return await crud.list_finds(db)

