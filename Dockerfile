FROM python:3.13.2-bookworm

# Set the working directory
WORKDIR /app

# Install dependencies: curl (for downloading Node.js)
RUN apt-get update && apt-get install -y curl

# Install Node.js and npm
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Verify installations
RUN node -v && npm -v && npx -v

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install uv

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uv", "run", "app.py", "--", "--host", "0.0.0.0", "--port", "8000"]

