# Base image for Python application
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /frontend

# Install dependencies directly
# V1 needs Flask and requests
RUN pip install --no-cache-dir Flask requests

# Copy the V1 application code and the templates folder
COPY FrontEnd_app.py .
# The HTML template is named index_v1.html
COPY templates ./templates 

# Expose the port the frontend runs on (5000)
EXPOSE 5000

# Define the command to run the application
ENTRYPOINT ["python"]
CMD ["FrontEnd_app.py"]
