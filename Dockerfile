FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/
COPY README.md LICENSE ./

# Create non-root user
RUN useradd -m -u 1000 agentjam && \
    chown -R agentjam:agentjam /app

USER agentjam

# Set Python path
ENV PYTHONPATH=/app/src

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Default command
ENTRYPOINT ["python", "-m", "agentjam.main"]
CMD ["--help"]
