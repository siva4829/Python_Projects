
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = os.getenv("DATABASE")
print(os.getenv("DATABASE"))
engine = create_async_engine(DATABASE_URL,echo=True)
sessionmakerLocal = sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with sessionmakerLocal() as session:
        yield session