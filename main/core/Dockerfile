#docker build -t microservices-img .
#docker run -p 5955:5955 -p 5957:5957 -p 5981:5981 microservices-img
FROM alpine:3.14

#ENV FILES_PATH /core
ENV FILES_PATH=
ENV DEST_PATH /usr/bin/

# Create a working directory for the Flask apps
WORKDIR /app

# Install dependencies for the Flask apps
RUN apk add --no-cache gcc musl-dev curl

RUN apk add --no-cache bash python3 py3-pip && \
    ln -s -f /usr/bin/python3 /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

RUN pip install loguru flask flask_httpauth gunicorn pyyaml requests

# Copy the source code for the Flask apps into the container
COPY $FILES_PATH/card_requests.html $DEST_PATH
COPY $FILES_PATH/card_requests.html /app
COPY $FILES_PATH/cards.yml $DEST_PATH
COPY $FILES_PATH/cards.yml /app
COPY $FILES_PATH/accounts.yml $DEST_PATH
COPY $FILES_PATH/accounts.yml /app
COPY $FILES_PATH/country.py $DEST_PATH
COPY $FILES_PATH/account.py $DEST_PATH
COPY $FILES_PATH/card.py $DEST_PATH
COPY $FILES_PATH/services.conf $DEST_PATH
COPY $FILES_PATH/services.conf /app
COPY $FILES_PATH/configuration.yml $DEST_PATH
COPY $FILES_PATH/configuration.yml /app

# Expose ports 5955, 5957, and 5981 for the Flask apps to listen on
EXPOSE 5955 5957 5981

# Install supervisor
RUN apk add --no-cache supervisor

RUN echo 'service account -> port 5957'
RUN echo 'service card -> port 5955'
RUN echo 'service country -> port 5981'

# Start supervisor to run all three Flask apps using gunicorn
CMD ["/usr/bin/supervisord", "-c", "/usr/bin/services.conf"]
