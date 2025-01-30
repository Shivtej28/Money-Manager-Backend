# Use an official Python runtime as a parent image
FROM python:3.10
RUN pip install --upgrade pip
RUN pip install db-sqlite3
RUN pip install psycopg2
RUN pip install alembic 
# Set the working directory in the container
WORKDIR /src

# Copy the current directory contents into the container
COPY . /src

# Install FastAPI and Uvicorn
RUN pip install -r ./requirements.txt

# Run database migrations
  # Make sure alembic is installed in your requirements.txt
# Expose port 8000 for the FastAPI app
EXPOSE 8000

# CMD alembic revision --autogenerate -m "description of change"
# CMD alembic upgrade head

# Command to run FastAPI with Uvicorn
CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
