## Environment
```
- Linux thinkpad-t480 5.4.0-81-generic #91~18.04.1-Ubuntu SMP Fri Jul 23 13:36:29 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
- Docker version 20.10.8, build 3967b7d
- Python 3.7.1
```

## How to run
- Install project dependencies
```bash
$ pip3 install -r requirements.txt
```
```bash
# Install protobuf compiler
$ sudo apt-get install protobuf-compiler

# Install buildtools
$ sudo apt-get install build-essential make
```
- Migrate database tables
```bash
$ cd rest/
$ make
$ python3 manage.py migrate
```
- Run the backend server
```bash
$ cd rest/
$ python3 manage.py runserver 127.0.0.1:8080
```

- Run the eclipse mosquitto docker container (add sudo at the front if needed)
```bash
$ cd MQTT/
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```

- Compile protobuf schema to python wrapper
```bash
$ cd gRPC/
$ make
```
- Start the fib service
```bash
$ cd gRPC/
$ python3 fib_server.py
```
- Start the log service
```bash
$ cd gRPC/
$ python3 log_server.py
```

## Send request
- Ask for the result of ﬁbonacci at N order
```bash
$ curl -X POST http://localhost:8080/rest/fibonacci  -d '{"order":N}'
```
- Get a list of history ﬁbonacci requests sent before
```bash
$ curl http://localhost:8080/rest/logs
```



# CommDesign
