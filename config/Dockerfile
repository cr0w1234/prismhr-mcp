# Use the official Python image
FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install the project into /app
COPY . /app
WORKDIR /app

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED=1
ENV PRISMHR_USERNAME="newtestuser"
ENV PRISMHR_PASSWORD="Newtestpassword1!"
ENV PRISMHR_PEO_ID="MKTPLC*TADAAI"
ENV PRISMHR_BASE_URL=https://salesdemoapi.prismhr.com/prismhr-api

# Install dependencies
RUN uv sync

# EXPOSE 8080

# Run the FastMCP server
CMD ["uv", "run", "small_prismhr_mcp_server.py"]