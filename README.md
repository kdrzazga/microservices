# Microservices
## A simple set of microservices for Docker, written in Python

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

4 microservices: 
- Account
- Card
- Country
- Credit Score

## Hosts
-   country: http://localhost:5981
-   card: http://localhost:5955
-   account: http://localhost:5957
-   credit-score: http://localhost:6011

## Installation

Require either Python 3 or Docker to run.

## How to run

Building an image:

```sh
docker build -t microservices-img .
```

Launching:

```sh
docker run -p 5955:5955 -p 5957:5957 -p 5981:5981 microservices-img
```

## License

MIT

**Free Software, Hell Yeah!**
