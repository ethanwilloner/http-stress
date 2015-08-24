#! /usr/bin/python3

import asyncio
import aiohttp
import argparse
import sys, time, os
from multiprocessing import Process, Value


# Coroutine which makes HTTP requests
@asyncio.coroutine
def request(url, connector):
    try:
        # HTTP Request Headers
        headers = {
                'User-Agent': "HTTP Stressing Agent/0.0.1"
                }

        response = yield from aiohttp.request('GET', url, headers=headers, connector=connector)
        response.close()
        return
   
    # If we cant resolve the URL
    except aiohttp.errors.ClientOSError as e:
        #print(e)
        None
    except Exception as e:
        #print(e)
        None

# Launches aiohttp coroutines
def agentRunner(args, totReq):
    try:
        # Create event loop for each Process
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)

        # Disable ssl checking
        connector = aiohttp.TCPConnector(verify_ssl=False)
        while totReq.value < args.requests:
            requests = []
            for _ in range(args.agents):
                if totReq.value >= args.requests:
                    break
                # Increment the total requests counter
                totReq.value += 1
                # Append request to list of futures
                requests.append(request(args.url, connector))
            # Wait for coroutines to finish 
            loop.run_until_complete(asyncio.wait(requests))

        loop.close()
    
    except KeyboardInterrupt:
        loop.stop()
        loop.close()
    
def threadScheduler(args):
    try:
        # Multiprocessing counter
        totReq = Value('i',0)
        # Thread list
        threads = []
        for _ in range(args.threads):
            t = Process(target=agentRunner, args=(args,totReq))
            threads.append(t)
            t.start()
   
        # Could be used to write a progress bar
        while totReq.value < args.requests:
            s = "Running..."
            sys.stdout.write(s)
            sys.stdout.flush()
            time.sleep(0.2)
            sys.stdout.write("\b" * len(s))

        sys.stdout.write("\n")
        
        # Wait for the threads to finish
        for t in threads:
            t.join()

    # Terminate all threads on Ctrl-C
    except KeyboardInterrupt:
        for t in threads:
            t.terminate
    

if __name__ == '__main__':
    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threads",
                        help="Number of Threads [Default 1]",
                        type=int,
                        default=1)
    parser.add_argument("-a", "--agents",
                        help="Apents per thread [Default 1]",
                        type=int,
                        default=1)
    parser.add_argument("-r", "--requests",
                        help="Total requests [Default 1]",
                        type=int,
                        default=1)
    parser.add_argument("url",
                        help="ex: https://example.com")
    args = parser.parse_args()
    
    # Disable tty echo 
    os.system("stty -echo")

    # Print runtime settings
    print("\tThreads: \t{}".format(args.threads))
    print("\tAgents/thread: \t{}".format(args.agents))
    print("\tRequests: \t{}".format(args.requests))
    print("\tHTTP Endpoint: \t{}".format(args.url))
    print()
  
    # Call thread scheduler 
    threadScheduler(args)
    # Re-enable tty echo
    os.system("stty echo")
    print()

    # Exit 
    sys.exit(0)
