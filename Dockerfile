# Use an official Python runtime as a parent image
FROM ubuntu

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt update
RUN apt install python3
RUN apt install python3-pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80


# Run app.py when the container launches
CMD ["python3", "app.py"]
