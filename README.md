# PAD Data Scraper Agent 🤖

AI Agent untuk mengambil data **Target dan Realisasi Pendapatan Asli Daerah (PAD)** dari dashboard [etax-klaten](https://dashboard.etax-klaten.id/monitoring_realisasi).

Built with **LangGraph** + **Clean Architecture**.

## Arsitektur

```
src/
├── domain/          # Entities & Port interfaces (no dependencies)
├── infrastructure/  # Playwright scraper implementation
├── application/     # Use cases (business logic orchestration)
└── agent/           # LangGraph state, tools, nodes, graph
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure API key
```bash
cp .env.example .env
# Edit .env dan masukkan OPENROUTER_API_KEY & DATABASE_URL
```

### 3. Run
dengan UI (recommended):
```bash
python app.py
```

dengan default message:
```bash
python main.py
```

dengan custom message:
```bash
python main.py "Ambil data PAD tahun 2026 dari https://dashboard.etax-klaten.id/monitoring_realisasi"
```

## Output

Agent akan mengembalikan JSON seperti:
```json
{
  "tahun": 2026,
  "sumber": "https://dashboard.etax-klaten.id/monitoring_realisasi",
  "data_target_realisasi_pad": [
    {
      "no": 1,
      "jenis_pajak": "Jasa Perhotelan",
      "target_rp": 1625000000,
      "realisasi_rp": 280688374,
      "persentase": "17.27%"
    }
  ],
  "total": {
    "target_rp": 336328350000,
    "realisasi_rp": 63188597032,
    "persentase": "18.79%"
  }
}
```

## Tech Stack

- **Python 3.11+**
- **LangGraph** — Stateful agent graph
- **Playwright** — Headless browser automation
- **Pydantic** — Data validation & serialization
- **Gradio** — UI

