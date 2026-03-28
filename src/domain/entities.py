"""Domain entities for PAD (Pendapatan Asli Daerah) data."""

from pydantic import BaseModel, Field


class PajakItem(BaseModel):
    """Represents a single tax type with its target and realization."""

    no: int = Field(description="Nomor urut")
    jenis_pajak: str = Field(description="Jenis pajak daerah")
    target_rp: int = Field(description="Target dalam Rupiah")
    realisasi_rp: int = Field(description="Realisasi dalam Rupiah")
    persentase: str = Field(description="Persentase realisasi terhadap target")


class TotalPAD(BaseModel):
    """Represents the total aggregation of PAD data."""

    target_rp: int = Field(description="Total target dalam Rupiah")
    realisasi_rp: int = Field(description="Total realisasi dalam Rupiah")
    persentase: str = Field(description="Persentase total realisasi")


class PADData(BaseModel):
    """Complete PAD (Pendapatan Asli Daerah) dataset for a given year."""

    tahun: int = Field(description="Tahun anggaran")
    sumber: str = Field(description="URL sumber data")
    data_target_realisasi_pad: list[PajakItem] = Field(
        description="Daftar data pajak per jenis"
    )
    total: TotalPAD = Field(description="Total keseluruhan")
