# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose port (if using FastAPI API)
EXPOSE 8000

# Default command (can change based on use case)
CMD ["python", "api.py"]