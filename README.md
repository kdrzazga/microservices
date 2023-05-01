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

```
+---------+       +---------+       +--------------+
| Country | ----> | Account | ----> | Credit Score |
|   5981  |       |   5957  |       |     6011     |
+---------+       +---------+       +--------------+
     ^                                     +-------+
     |                                     | Cards |
     +-------------------------------------| 5955  |
                                           +-------+
```

## Installation

Requires either Python 3 or Docker

## How to run

Building an image:

```sh
docker build -t microservices-img .
docker build -t microservices-aux .
```

Launching:

```sh
docker run -p 5955:5955 -p 5957:5957 -p 5981:5981 microservices-img
docker run -p 6011:6011 microservices-aux
```


> Note: `resources/microservices-py.postman_collection.json` contains set of REST requests to be imported into Postman

## License

MIT

**Free**
