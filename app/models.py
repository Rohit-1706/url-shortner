from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class URL(Base):
    __tablename__ = "urls"

    id          = Column(Integer, primary_key=True, index=True)
    code        = Column(String(10), unique=True, index=True, nullable=False)
    original    = Column(String(2048), nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())


    # we store clicks count in redis for speed
    # this column holds the "flushed " count for persistence
    clicks = Column(Integer, default=0)
    expires_at  = Column(DateTime(timezone=True), nullable=True)



# The code index = True- because every redirect does where coe = "" and  without index it will scan the whole table.