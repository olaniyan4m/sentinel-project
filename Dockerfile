# Sentinel Web Application Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create data directory
RUN mkdir -p real_data

# No database setup needed - using Firebase only

# Create Streamlit config directory
RUN mkdir -p /root/.streamlit

# Create Streamlit config to disable telemetry
RUN echo "[browser]" > /root/.streamlit/config.toml && \
    echo "gatherUsageStats = false" >> /root/.streamlit/config.toml && \
    echo "[server]" >> /root/.streamlit/config.toml && \
    echo "headless = true" >> /root/.streamlit/config.toml && \
    echo "port = 8501" >> /root/.streamlit/config.toml && \
    echo "address = \"0.0.0.0\"" >> /root/.streamlit/config.toml

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "sentinel_web_app_firebase_only.py", "--server.port=8501", "--server.address=0.0.0.0"]
