# Binance stream logger #

## Goal ##

Create a simple local orderbook API that interfaces with th Binance live exchange.
The engine fetches a snapshot of the orderbook and 
then maintains a local copy using updates from a websocket stream.

Also, the goal is to have a simple API that lets to query the volume 
available at a certain price or up to a certain price.

## Architecture ##

The project was done using the [microservices architectural pattern][microservices_article].

It is common to use HTTP (and REST), but as we’ll see, 
we can use other types of communication protocols such as RPC (Remote Procedure Call) 
over AMQP (Advanced Message Queuing Protocol).

For that, we will use [Nameko][nameko], a Python microservices framework. 
It has RPC over AMQP built in, allowing for you to easily communicate between your services. 
It also has a simple interface for HTTP queries, which we’ll use in this project for simplicity. 
However, for writing Microservices that expose an HTTP endpoint, 
it is recommended that you use another framework, such as [Flask][flask] or [FastAPI][fastapi]. 
To call Nameko methods over RPC using Flask, you can use [flask_nameko][flask_nameko], 
a wrapper built just for interoperating Flask with Nameko.

Also, Nameko allows to scale the service very easily.
Nameko is built to robustly handle methods calls in a cluster.
It’s important to build services with some backward compatibility in mind, 
since in a production environment it can happen for several different versions of the same 
service to be running at the same time, especially during deployment. 
If you use Kubernetes, during deployment it will only kill all the old version containers 
when there are enough running new containers.

For Nameko, having several different versions of the same service running at the same 
time is not a problem. Since it distributes the calls in a round-robin fashion, 
the calls might go through old or new versions. 

The service classes are instantiated at the moment a call is made and destroyed after 
the call is completed. 
Therefore, they should be inherently stateless, meaning you should not try to keep any 
state in the object or class between calls. 
This implies that the services themselves must be stateless. 
With the assumption that all services are stateless, 
Nameko is able to leverage concurrency by using [eventlet][eventlet] greenthreads. 
The instantiated services are called “workers,” and there can be a configured maximum 
number of workers running at the same time.

## Requirements

* [Docker][docker]
* [Docker-compose][docker-compose]

### Running

```shell script
$ docker-compose up
```

or 

```shell script
$ docker-compose up -d
```
if you don't want to see logs.

In case of running with logs after the build you'll 
see the information about the snapshot and messages from the stream:

```shell script
binance-stream-listener | Order book received: 1000 bids and 1000 asks.
binance-stream-listener | {'e': 'depthUpdate', 'E': 1636584721215, 's': 'BNBBTC', 'U': 2316807568, 'u': 2316807594, 'b': [['0.00933000', '4.98000000'], ['0.00932800', '6.50900000'], ['0.00932600', '11.57000000'], ['0.00925200', '54.64300000'], ['0.00925000', '7.61600000'], ['0.00919800', '13.76300000'], ['0.00918800', '3.98000000']], 'a': [['0.00933800', '0.00000000'], ['0.00933900', '1.06900000'], ['0.00934000', '7.90100000'], ['0.00934100', '8.19700000'], ['0.00934400', '6.33200000'], ['0.00934500', '18.06700000'], ['0.00935300', '0.34700000']]}
binance-stream-listener | {'e': 'depthUpdate', 'E': 1636584722215, 's': 'BNBBTC', 'U': 2316807595, 'u': 2316807607, 'b': [['0.00933200', '1.24900000'], ['0.00933100', '0.00000000'], ['0.00932900', '10.01700000'], ['0.00932700', '14.25900000'], ['0.00932400', '7.54200000'], ['0.00906500', '89.90000000']], 'a': [['0.00933800', '0.37400000'], ['0.00933900', '1.06900000'], ['0.00934000', '13.25600000'], ['0.00934300', '28.47800000'], ['0.00934400', '7.57000000']]}
```

Then after it's up and you have records in the DB you can use the volume endpoint to get the volume:

```
http://localhost:8003/volume/<type:a|b>?price=<price>&operator=<operator:lte|eq>
```

```shell script
$ curl 'http://localhost:8003/volume/a?price=0.0098&operator=eq'
[{"total": 0.0098, "volume": 35.447}]        
```
```shell script
$ curl 'http://localhost:8003/volume/a?price=0.0098&operator=lte'
[{"total": 4.18631, "volume": 3071.491}]
```

Also get order endpoint is available:
```shell script
$ curl 'http://localhost:8003/orders/1'                         
{"price": 0.009298, "id": 1, "cc": "bnbbtc", "type": "a", "quantity": 18.004}% 
```
```shell script
$ curl 'http://localhost:8003/orders/1324245452454'
{"error": "UNEXPECTED_ERROR", "message": "NotFound Order with id 1324245452454 not found"}%
```

### Tests

```shell script
$ make test
```
or
```shell script
$ make coverage
```
to run the tests with coverage report

### Service shell

```shell script
$ docker-compose exec logger bash
```
```shell script
nameko shell --config config.yml
```

```shell script
root@4da5fbe878aa:/app# nameko shell --config config.yml
Nameko Python 3.9.7 (default, Oct 13 2021, 09:00:49) 
[GCC 10.2.1 20210110] shell on linux
Broker: amqp://guest:guest@rabbit:5672/ (from --config)
>>> 
```

And to interact with a service inside nameko shell:

```shell script
 n.rpc.logger.get_volume('a', 0.0096, 'eq')
```

It will give the volume.
```shell script
>>> n.rpc.logger.get_volume('a', 0.0096, 'eq')
[{'volume': 160.16400000000002, 'total': 0.12479999999999998}]
```

You can access all the services.
Use exit() or Ctrl-D (i.e. EOF) to exit.

### DB shell

```shell script
$ docker-compose exec postgres bash
```
Enter Postgres
```shell script
psql -U postgres
```
Use the app db
```shell script
\c binance_stream_db
```
Run queries
```shell script
docker-compose exec postgres bash
root@39f59ec1442a:/# psql -U postgres
psql (14.0 (Debian 14.0-1.pgdg110+1))
Type "help" for help.

postgres=# \c binance_stream_db 
You are now connected to database "binance_stream_db" as user "postgres".
binance_stream_db=# SELECT sum(orders.quantity) AS volume, sum(orders.price) AS total FROM orders WHERE orders.type = 'a' AND price = 0.0096;
 volume | total  
--------+--------
 50.986 | 0.0096
(1 row)

```

### To Do

* Add Flask or Fast API with a proper validation, sorting, filtering and schemas
* Add Flasgger documentation
* Add CI/CD
* Add Swagger documentation
* Add more unit and functional tests
* All variables in .env
* Catch negative use case scenarios
* Add k8s to manage containers
* Fix wait-for-it functionality

[microservices_article]: https://martinfowler.com/articles/microservices.html
[nameko]: https://nameko.readthedocs.io/en/stable/
[flask]: https://flask.palletsprojects.com/en/1.1.x/
[fastapi]: https://fastapi.tiangolo.com/
[flask_nameko]: https://github.com/jessepollak/flask-nameko
[eventlet]: http://eventlet.net/
[docker]: https://docs.docker.com/get-docker/
[docker-compose]: https://docs.docker.com/compose/install/