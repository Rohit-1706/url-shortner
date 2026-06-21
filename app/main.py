from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager

from app.database import engine, get_db, Base
from app.models import URL
from app.schemas import ShortenRequest, ShortenResponse, StatsResponse
from app.cache import get_cached_url, set_cached_url, increment_clicks, get_clicks_count
from app.shortner import generate_code

import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="URL Shortner", lifespan=lifespan)
BASE_URL = os.getenv("BASE_URL")


@app.post("/shorten", response_model=ShortenResponse, status_code=201)
async def shorten_url(request: ShortenRequest, db: AsyncSession = Depends(get_db)):
    url_str = str(request.url)

    for _ in range(5):
        code = generate_code()
        result = await db.execute(select(URL).where(URL.code == code))
        if not result.scalar_one_or_none():
            break
    else:
        raise HTTPException(500, "Could not generate unique code")

    
    url_obj = URL(code=code, original=url_str)
    db.add(url_obj)
    await db.commit()
    await db.refresh(url_obj)

    await set_cached_url(code, url_str)

    return ShortenResponse(
        code=code,
        short_url=f"{BASE_URL}/{code}",
        original_url=url_str
    )


@app.get("/stats/{code}", response_model=StatsResponse)
async def stats(code: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(URL).where(URL.code == code))
    url_obj = result.scalar_one_or_none()
    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")
    
    clicks = await get_clicks_count(code)

    return StatsResponse(
        code=code,
        original_url=url_obj.original,
        clicks=clicks,
        created_at=url_obj.created_at

    )

@app.get("/{code}")
async def redirect(code: str, db: AsyncSession = Depends(get_db)):
    original = await get_cached_url(code)

    if not original:
        result = await db.execute(select(URL).where(URL.code == code))
        url_obj = result.scalar_one_or_none()
        if not url_obj:
            raise HTTPException(status_code=404, detail="URL not found")
        original = url_obj.original
        await set_cached_url(code, original)

    await increment_clicks(code)
    return RedirectResponse(url=original, status_code=302)
