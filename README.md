# http-stress

http-stress is a simple python3 application which uses asyncio and aiohttp to concurrently make hundreds or thousands of connections to an http or https web server.

# Requirements
```
sudo pip3 install aiohttp
```

# Usage
```
./http-stress.py -h
usage: http-stress.py [-h] [-t THREADS] [-a AGENTS] [-r REQUESTS] url

positional arguments:
  url                   ex: https://example.com

optional arguments:
  -h, --help            show this help message and exit
  -t THREADS, --threads THREADS
                        Number of Threads [Default 1]
  -a AGENTS, --agents AGENTS
                        Apents per thread [Default 1]
  -r REQUESTS, --requests REQUESTS
                        Total requests [Default 1]

```
# Version 
0.0.1
