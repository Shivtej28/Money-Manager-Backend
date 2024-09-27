# Use an official Python runtime as a parent image
FROM python:3.10
RUN pip install --upgrade pip
RUN pip install db-sqlite3
# Set the working directory in the container
WORKDIR /money-maanager-api

# Copy the current directory contents into the container
COPY . /money-manager-api

# Install FastAPI and Uvicorn
RUN pip install -r requirements.txt

# RUN alembic revision --autogenerate -m "description of change"
# Run database migrations
RUN alembic upgrade head  # Make sure alembic is installed in your requirements.txt
# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
