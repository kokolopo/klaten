"""LangGraph tools for the PAD scraper agent."""

from datetime import datetime

from langchain_core.tools import tool

from langchain_core.runnables import RunnableConfig

from src.application.use_cases import ScrapeRealisasiPAD
from src.infrastructure.database import PostgresRepository
from src.infrastructure.scraper import PlaywrightScraper


@tool
async def scrape_pad_realisasi(url: str, tahun: int, config: RunnableConfig) -> str:
    """Scrape data Target dan Realisasi PAD dari halaman dashboard etax.

    Membuka halaman web menggunakan browser otomatis, mengekstrak
    tabel data pajak daerah, menyimpannya ke database, dan mengembalikan 
    hasilnya sebagai JSON.

    Args:
        url: URL halaman dashboard, contoh: https://dashboard.etax-klaten.id/monitoring_realisasi
        tahun: Tahun anggaran yang ingin diambil datanya, contoh: 2026
    """
    scraper = PlaywrightScraper()
    db = None
    
    # Check if UI requested to save to DB via config
    save_to_db = config.get("configurable", {}).get("save_to_db", False)
    
    if save_to_db:
        try:
            db = PostgresRepository()
        except ValueError:
            pass  # Fallback to None if DATABASE_URL is missing

    use_case = ScrapeRealisasiPAD(scraper=scraper, db=db)
    result = await use_case.execute_as_json(url=url, tahun=tahun)
    return result


@tool
def get_current_year() -> int:
    """Mendapatkan tahun saat ini. Berguna untuk menentukan tahun anggaran."""
    return datetime.now().year


# Registry of all tools available to the agent
ALL_TOOLS = [scrape_pad_realisasi, get_current_year]
