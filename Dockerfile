FROM python:3.13-slim

# Install Tesseract + dependencies
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Set working directory
WORKDIR /app

# Copy requirements & install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose port
ENV PORT 5000
EXPOSE $PORT

# Run the app
CMD ["python", "app.py"]
