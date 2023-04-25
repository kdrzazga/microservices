FROM alpine:3.14

# Create a working directory for the Flask app
WORKDIR /app

# Install dependencies for the Flask app
RUN apk add --no-cache gcc musl-dev curl

# Install Python 3 and pip
RUN apk add --no-cache bash python3 py3-pip && \
    ln -s -f /usr/bin/python3 /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

# Install required Python packages
RUN pip install flask

# Copy the Flask app code into the container
COPY aux_img/credit_score.py .

# Expose port 5000 for the Flask app to listen on
EXPOSE 5000

# Start the Flask app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "credit_score:app"]
