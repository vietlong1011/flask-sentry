
FROM python:3.10

# Set the working directory within the container
WORKDIR /flask/app

# Copy the necessary files and directories into the container
COPY app/ /flask/app/
# COPY app/static/ /flask/app/static/
# COPY app/instance/test.db /flask/app/instance/test.db
# COPY py3.10.12/ /flask/py3.10.12/
COPY requirements.txt requirements.txt
# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000


# Define the command to run the Flask application using Gunicorn
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "-w", "4"]