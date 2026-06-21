from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# engine is the actual connection to postgres
# pool size means no of connections
# without pooling every request would open and close a tcp connection
engine = create_async_engine(DATABASE_URL, pool_size=5, max_overflow=10)

# a session is connection with the db
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_= AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass

# fastapi dependency gives each request its own DB session
# then close it when the request is done

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


    

