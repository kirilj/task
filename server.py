

import requests
import time
from enum import Enum
import argparse

from requests.models import Response

DefaultSamplesPerMinute = 30

class ServerStatus(Enum):
    ResponseOK = 1
    ResponseError = 2
    ServerDown = 3

# A class that collect statistics about server health over time 
class Statistics:
    Successes = 0
    Failures = 0
    ServerDown = 0
    SamplesTaken = 0
    SamplesPerMinute = 0

    def __init__(self, samplesPerMinute):
        self.SamplesPerMinute = samplesPerMinute

    def resetMetrics(self):
        self.SamplesTaken = 0
        self.Successes = 0
        self.Failures = 0
        self.ServerDown = 0

    def collecStatistics(self, serverStatus):

        self.SamplesTaken = self.SamplesTaken + 1
        if serverStatus == ServerStatus.ResponseOK:
            self.Successes = self.Successes + 1
        elif serverStatus == ServerStatus.ResponseError: 
            self.Failures = self.Failures + 1
        else:
            self.ServerDown = self.ServerDown + 1
        
        if self.SamplesTaken == self.SamplesPerMinute: 
            print 'Total Samples:', self.SamplesTaken, ', Number of valid responses:', self.Successes, ', Number of error responses:', self.Failures, ', Number of times server was down:', self.ServerDown
        
            self.resetMetrics()

def checkWebServerHealth(ServerUrl, statistics):
    try:
        response = requests.get(ServerUrl)

        handleResponse(response, statistics, ServerUrl)

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        print 'Server', ServerUrl, 'is down'
        statistics.collecStatistics(ServerStatus.ServerDown)


def handleResponse(response, statistics, ServerUrl):
    if response.status_code != 200:
        print 'Error', response.status_code, 'reason', response.reason, ServerUrl
        statistics.collecStatistics(ServerStatus.ResponseOK)
    else:
        print 'All okay'
        statistics.collecStatistics(ServerStatus.ResponseError)

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, help="web server's health to check", required=True)
    parser.add_argument("--samples", type=int, help="samples per minute", default=DefaultSamplesPerMinute)
    args = parser.parse_args()
    return args.url, args.samples


# Program main function
def main():
    url, samplesPerMinute = parseArguments()

    sleepInterval = 60 / samplesPerMinute

    statistics = Statistics(samplesPerMinute)

    while True:
        try:
            checkWebServerHealth(url, statistics)
            time.sleep(sleepInterval)
        
        except KeyboardInterrupt:
            print 'exited'
            break

if __name__ == "__main__":
    main()
