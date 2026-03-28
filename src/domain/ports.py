"""Port interfaces (abstract contracts) for the domain layer."""

from abc import ABC, abstractmethod

from src.domain.entities import PADData


class ScraperPort(ABC):
    """Abstract interface for scraping PAD data from a web source."""

    @abstractmethod
    async def scrape_pad_data(self, url: str, tahun: int) -> PADData:
        """Scrape PAD target & realisasi data from the given URL.

        Args:
            url: The dashboard URL to scrape.
            tahun: The fiscal year to extract data for.

        Returns:
            PADData containing all tax items and totals.

        Raises:
            ScrapingError: If data extraction fails.
        """


class DatabasePort(ABC):
    """Abstract interface for storing PAD data to a database."""

    @abstractmethod
    async def save_pad_data(self, data: PADData) -> None:
        """Save the extracted PAD data into the database.

        This should update targets and insert/update realizations
        for the given year based on the tax types.

        Args:
            data: The parsed PAD data to save.
            
        Raises:
            DatabaseError: If there's an issue executing the database operations.
        """
