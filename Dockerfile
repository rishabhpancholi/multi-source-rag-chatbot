# Base python image
FROM python:3.12-slim

# Setting the working directory inside the container
WORKDIR /api

# Copying the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copying the FastAPI app code into the container
COPY api/ ./api/

# Command to run the FastAPI app using uvicorn

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


