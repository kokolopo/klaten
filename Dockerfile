# Gunakan base image resmi dari Microsoft yang sudah dilengkapi OS dependencies untuk Playwright
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set direktori kerja di dalam container
WORKDIR /app

# Copy daftar dependency terlebih dahulu untuk memanfaatkan Docker cache
COPY requirements.txt .

# Install seluruh PyPI packages (termasuk Gradio, LangGraph, Playwright, dll)
RUN pip install --no-cache-dir -r requirements.txt

# Download binary browser Chromium Playwright di tahap build agar boot-time server lebih cepat
RUN playwright install chromium

# Copy seluruh file project ke dalam container
COPY . .

# Beritahu Docker bahwa aplikasi Gradio akan berjalan di port 7860
EXPOSE 7860

# Wajib untuk Gradio di dalam Docker agar bisa diakses dari luar (mengikat ke 0.0.0.0)
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Jalankan aplikasi utama
CMD ["python", "app.py"]
