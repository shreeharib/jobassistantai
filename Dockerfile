# Use an official Python image as a base
FROM python:3.11.3

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose the port your application will use
EXPOSE 8000

# Run the command to start your application
CMD ["streamlit", "run", "app.py"]