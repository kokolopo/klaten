"""Application use cases for PAD data operations."""

from src.domain.entities import PADData
from src.domain.ports import DatabasePort, ScraperPort


class ScrapeRealisasiPAD:
    """Use case: Scrape PAD target & realisasi data from dashboard.

    Orchestrates the scraping process through the ScraperPort interface,
    keeping the business logic decoupled from infrastructure details.
    """

    def __init__(self, scraper: ScraperPort, db: DatabasePort | None = None) -> None:
        self._scraper = scraper
        self._db = db

    async def execute(self, url: str, tahun: int) -> PADData:
        """Execute the scraping use case.

        Args:
            url: Dashboard URL to scrape.
            tahun: Fiscal year to extract.

        Returns:
            PADData with complete target & realisasi information.
        """
        # Scrape the data
        data = await self._scraper.scrape_pad_data(url=url, tahun=tahun)
        
        # Save to database if configured
        if self._db:
            await self._db.save_pad_data(data)
            
        return data

    async def execute_as_json(self, url: str, tahun: int) -> str:
        """Execute and return result as formatted JSON string."""
        data = await self.execute(url=url, tahun=tahun)
        return data.model_dump_json(indent=2)
