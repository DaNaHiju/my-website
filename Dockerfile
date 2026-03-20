# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependency file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to ensure output is flushed
ENV PYTHONUNBUFFERED=1

# Run the application
# We use python -m flask run to bind to 0.0.0.0 so it's accessible from outside the container
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
