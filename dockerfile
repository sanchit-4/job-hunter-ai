# 1. Base Image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install System Dependencies (wkhtmltopdf + Playwright deps)
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements
COPY requirements.txt .

# 5. Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Install Playwright Browsers
RUN playwright install chromium
RUN playwright install-deps

# 7. Copy App Code
COPY . .

# 8. Create folder for generated files
RUN mkdir -p generated_applications

# 9. Run the Server
# Render uses port 10000 by default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]