#To install this image, execute command
# docker build -t python-app-img .
#run and access it in with
# docker run -it --memory=300m --cpus=0.5 python-app-img
# docker run -p 8080:8080 python-app-img
FROM alpine:3.14

# Install required packages (wget, curl, nano, git and python + pip + pytest)
RUN apk update && \
    apk add --no-cache wget unzip && \
    rm -rf /var/cache/apk/*

RUN apk add curl
RUN apk add nano
RUN apk add git

RUN apk add --no-cache bash python3 py3-pip && \
    ln -s -f /usr/bin/python3 /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

RUN pip install --no-cache-dir pytest

# Check installed programs
RUN nano --version
RUN git --version
RUN python --version
RUN pip --version
RUN pytest --version

# Create directory
RUN rm -rf /usr/share/python-code #remove old one
RUN mkdir -p /usr/share/python-code
WORKDIR /usr/share/python-code

# Create user
RUN addgroup -g 10000 testers && \
    adduser -u 10000 -G testers -s /bin/sh -D userX
RUN chown -R userX:testers /usr/share/python-code
RUN chmod 777 /usr/share/python-code

# Get the app code

USER userX

##Running tests
RUN pip install -r requirements.txt
RUN pytest -m unit --junitxml=unittest-result.xml --maxfail=9999
