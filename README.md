# What it does

The python script monitors the health of a given web server. It performs a health check X times
a minute. I takes as arguments the web server url to monitor, and how many checks to perform a minute. 
It prints the latest state and the overall state durig the last period of time.

# System prerequisites

python 3.6

# How to run it

python server.py --url='web server url to monitor' --samples=NumberOfSamplesAMinute

example:

python server.py --url='https://fake.url' --samples=30