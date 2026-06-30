# Multi-stage build for optimization
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
COPY apt.txt .
RUN apt-get update && \
    xargs -a apt.txt apt-get install -y --no-install-recommends || echo "No apt.txt file or no packages to install" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

# Copy system dependencies from builder stage
COPY --from=builder /usr/bin/wkhtmltopdf /usr/bin/wkhtmltopdf 2>/dev/null || echo "wkhtmltopdf not available"
COPY --from=builder /usr/bin/xvfb-run /usr/bin/xvfb-run 2>/dev/null || echo "xvfb-run not available"
COPY --from=builder /usr/lib/x86_64-linux-gnu/lib* /usr/lib/x86_64-linux-gnu/ 2>/dev/null || echo "No lib files to copy"
COPY --from=builder /usr/lib/lib* /usr/lib/ 2>/dev/null || echo "No lib files to copy"
COPY --from=builder /usr/share/wkhtmltopdf /usr/share/wkhtmltopdf 2>/dev/null || echo "wkhtmltopdf assets not available"
COPY --from=builder /etc/fonts /etc/fonts 2>/dev/null || echo "Font files not available"
COPY --from=builder /usr/share/fonts /usr/share/fonts 2>/dev/null || echo "Font files not available"

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Create .env file if it doesn't exist
RUN if [ ! -f .env ]; then cp .env.example .env; fi

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run app
ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
