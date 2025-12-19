"""
AUREA PRIME ELITE - Database Manager
=====================================
Main database connection and initialization
"""

import aiosqlite
import asyncio
from pathlib import Path
from loguru import logger
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import DATABASE_PATH


class DatabaseManager:
    """Async SQLite Database Manager"""
    
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(self):
        """Initialize database connection"""
        if self._db is None:
            db_path = Path(DATABASE_PATH)
            db_path.parent.mkdir(parents=True, exist_ok=True)
            
            self._db = await aiosqlite.connect(DATABASE_PATH)
            self._db.row_factory = aiosqlite.Row
            await self._init_tables()
            logger.info(f"Database connected: {DATABASE_PATH}")
        return self._db
    
    async def _init_tables(self):
        """Initialize database tables from schema"""
        schema_path = Path(__file__).parent / "schema.sql"
        
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema = f.read()
            await self._db.executescript(schema)
            await self._db.commit()
            logger.info("Database tables initialized")
    
    async def execute(self, query: str, params: tuple = None):
        """Execute a query"""
        db = await self.connect()
        cursor = await db.execute(query, params or ())
        await db.commit()
        return cursor
    
    async def fetchone(self, query: str, params: tuple = None):
        """Fetch single row"""
        db = await self.connect()
        cursor = await db.execute(query, params or ())
        return await cursor.fetchone()
    
    async def fetchall(self, query: str, params: tuple = None):
        """Fetch all rows"""
        db = await self.connect()
        cursor = await db.execute(query, params or ())
        return await cursor.fetchall()
    
    async def close(self):
        """Close database connection"""
        if self._db:
            await self._db.close()
            self._db = None
            logger.info("Database connection closed")


db = DatabaseManager()

async def get_db() -> DatabaseManager:
    """Get database instance"""
    await db.connect()
    return db
