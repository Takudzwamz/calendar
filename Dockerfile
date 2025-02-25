# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Define the argument for the Flask secret key
ARG FLASK_SECRET_KEY

# Set the working directory in the container
WORKDIR /usr/src/app

# Set the Flask secret key as an environment variable
ENV FLASK_SECRET_KEY=$FLASK_SECRET_KEY

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

# Run app.py when the container launches
CMD ["python", "./app.py", "0.0.0.0:80"]
