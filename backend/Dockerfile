# Base image from a Python slim distribution
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /backend

# Copy the requirements file and install dependencies
RUN pip install --no-cache-dir Flask

# Copy the application code
COPY BackEnd_app.py .

# The backend runs on port 5001
EXPOSE 5001

# Define the command to run the application
# We run the app.py file directly with python
ENTRYPOINT ["python"]
CMD ["BackEnd_app.py"]
