FROM python:3.8-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.

COPY ./ /home/upload-flask-api/
WORKDIR /home/upload-flask-api/

# Install production dependencies.
RUN pip3 install  -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
# tell the port number the container should expose
EXPOSE 8080

# run the application
CMD ["python", "/home/upload-flask-api/main.py"]
