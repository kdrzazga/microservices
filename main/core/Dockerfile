# docker build -t 3micro-img .
# docker run -p 5955:5955 -p 5957:5957 -p 5981:5981 3micro-img
# docker run -it 3micro-img

FROM alpine:3.14

# Create a working directory for the Flask apps
WORKDIR /app

# Install dependencies for the Flask apps
RUN apk add --no-cache gcc musl-dev curl

RUN apk add --no-cache bash python3 py3-pip && \
    ln -s -f /usr/bin/python3 /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

RUN pip install flask flask_httpauth gunicorn pyyaml loguru

# Copy the source code for the Flask apps into the container
COPY core/cards.yml ./
COPY core/country.py ./
COPY core/account.py ./
COPY core/card.py ./

# Expose ports 5955, 5957, and 5981 for the Flask apps to listen on
EXPOSE 5955 5957 5981

# Copy the supervisor configuration file into the container
#COPY services.conf /etc/supervisor/conf.d/
# Install supervisor
RUN apk add --no-cache supervisor

COPY core/services.conf /usr/bin/

RUN echo 'service account -> port 5957'
RUN echo 'service card -> port 5955'
RUN echo 'service country -> port 5981'

# Start supervisor to run all three Flask apps using gunicorn
CMD ["/usr/bin/supervisord", "-c", "/usr/bin/services.conf"]
