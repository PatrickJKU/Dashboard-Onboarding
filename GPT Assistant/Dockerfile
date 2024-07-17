# Use an official Python runtime as a parent image
FROM python:3.9.7

# Set the working directory in the container
WORKDIR /GPT Assistant/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "GPT_V2.py"]