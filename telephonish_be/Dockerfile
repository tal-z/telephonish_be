FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a directory for the code
WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the code into the container
COPY . .

# Start the server with Daphne
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "collectstatic", "--no-input"]
CMD ["daphne", "telephonish_be.telephonish_be.asgi:application", "-b", "0.0.0.0", "-p", "8000"]
