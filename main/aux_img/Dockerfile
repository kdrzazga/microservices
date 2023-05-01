#docker build -t microservices-aux .
#docker run -p 6011:6011 microservices-aux
FROM alpine:3.14

# Create a working directory for the Flask app
WORKDIR /app

# Install dependencies for the Flask app
RUN apk add --no-cache gcc musl-dev curl python3-dev build-base linux-headers

# Install Python 3 and pip
RUN apk add --no-cache bash python3 py3-pip && \
    ln -s -f /usr/bin/python3 /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

# Install required Python packages
RUN pip install flask loguru uwsgi pyyaml

# Copy the Flask app code into the container
COPY credit_score.py .
COPY configuration.yml .

# Expose port 6011 for the Flask app to listen on
EXPOSE 6011

# Use uwsgi to start the Flask app
CMD ["uwsgi", "--http", "0.0.0.0:6011", "--wsgi-file", "credit_score.py", "--callable", "app", "--master", "--processes", "4", "--threads", "2"]
