"""PostgreSQL database repository implementation."""

import os
from typing import Any

import asyncpg

from src.domain.entities import PADData
from src.domain.ports import DatabasePort


class DatabaseError(Exception):
    """Raised when a database operation fails."""


class PostgresRepository(DatabasePort):
    """Saves PAD data to PostgreSQL using asyncpg."""

    def __init__(self, dsn: str | None = None) -> None:
        """Initialize the repository.
        
        Args:
            dsn: PostgreSQL connection string. If None, uses DATABASE_URL from environment.
        """
        self.dsn = dsn or os.getenv("DATABASE_URL")
        if not self.dsn:
            raise ValueError("DATABASE_URL must be set if no DSN is provided.")

    async def save_pad_data(self, data: PADData) -> None:
        """Save the extracted PAD data into the database."""
        try:
            # Connect to database
            conn = await asyncpg.connect(self.dsn)
            try:
                # Use a transaction so all updates succeed or fail together
                async with conn.transaction():
                    for item in data.data_target_realisasi_pad:
                        # 1. Look up the tax type ID by name
                        # We use ILIKE or standard matching, depending on exact string match
                        # First try exact
                        row = await conn.fetchrow(
                            "SELECT id FROM master_pajak WHERE nama_pajak = $1",
                            item.jenis_pajak,
                        )
                        
                        # If not found exactly, try case-insensitive
                        if not row:
                            row = await conn.fetchrow(
                                "SELECT id FROM master_pajak WHERE nama_pajak ILIKE $1",
                                item.jenis_pajak,
                            )
                            
                        # If still not found, we could insert it or just log warning/skip
                        if not row:
                            print(f"⚠️ Warning: Pajak '{item.jenis_pajak}' tidak ditemukan di tabel master_pajak. Menambahkan entri baru...")
                            new_id = await conn.fetchval(
                                "INSERT INTO master_pajak (nama_pajak, type_id) VALUES ($1, $2) RETURNING id",
                                item.jenis_pajak, 
                                1  # Default to Pajak Daerah
                            )
                            pajak_id = new_id
                        else:
                            pajak_id = row['id']
                            
                        # 2. Upsert target_pajak
                        # Uses ON CONFLICT to update if it already exists for this id_pajak+tahun
                        await conn.execute(
                            """
                            INSERT INTO target_pajak (id_pajak, tahun, target_rp)
                            VALUES ($1, $2, $3)
                            ON CONFLICT (id_pajak, tahun) 
                            DO UPDATE SET target_rp = EXCLUDED.target_rp
                            """,
                            pajak_id,
                            data.tahun,
                            item.target_rp
                        )
                        
                        # 3. Insert realisasi_pajak
                        await conn.execute(
                            """
                            INSERT INTO realisasi_pajak (id_pajak, tahun, realisasi_rp, tanggal_input)
                            VALUES ($1, $2, $3, CURRENT_TIMESTAMP)
                            """,
                            pajak_id,
                            data.tahun,
                            item.realisasi_rp
                        )
            finally:
                await conn.close()
        except Exception as e:
            raise DatabaseError(f"Gagal menyimpan data ke database PostgreSQL: {str(e)}") from e
