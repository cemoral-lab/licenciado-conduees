import os

from sqlalchemy import Column, DateTime, Integer, String, Text, func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./licenciado.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Mensaje(Base):
    __tablename__ = "mensajes"

    id = Column(Integer, primary_key=True, index=True)
    telefono = Column(String(50), index=True, nullable=False)
    role = Column(String(20), nullable=False)  # "user" | "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())


async def inicializar_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def guardar_mensaje(telefono: str, role: str, content: str):
    async with AsyncSessionLocal() as session:
        msg = Mensaje(telefono=telefono, role=role, content=content)
        session.add(msg)
        await session.commit()


async def obtener_historial(telefono: str, limite: int = 20) -> list[dict]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Mensaje)
            .where(Mensaje.telefono == telefono)
            .order_by(Mensaje.timestamp.desc())
            .limit(limite)
        )
        rows = result.scalars().all()
        return [{"role": m.role, "content": m.content} for m in reversed(rows)]


async def limpiar_historial(telefono: str):
    from sqlalchemy import delete
    async with AsyncSessionLocal() as session:
        await session.execute(delete(Mensaje).where(Mensaje.telefono == telefono))
        await session.commit()
