FROM python:3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update

# Create and set working directory
WORKDIR /base

# Install Python dependencies
COPY requirements.txt /base/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /base/

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]