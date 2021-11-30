import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

#add
MQTT_PORT = 1883
history = []

def on_message(client, obj, msg):
    order = str(msg.payload)
    order = order[2:-1]
    #print(order)
    history.append(int(order))
'''
def main():
    # Establish connection to mqtt broker
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host='127.0.0.1', port=MQTT_PORT)
    client.subscribe('history', 0)
    
    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass
    
'''
#

class LogCalculatorServicer(log_pb2_grpc.LogCalculatorServicer):

    def __init__(self):
        pass
    '''orig
    def Compute(self, request, context):
        n = request.order
        value = self._fibonacci(n)

        response = fib_pb2.FibResponse()
        response.value = value

        return response
    '''
    #add
    def Compute(self, request, context):
        response = log_pb2.LogResponse()
        for h in history: 
            response.data.append(h)

        return response
    #

    '''
    def _fibonacci(self, n):
        a = 0
        b = 1
        if n < 0:
            return 0
        elif n == 0:
            return 0
        elif n == 1:
            return b
        else:
            for i in range(1, n):
                c = a + b
                a = b
                b = c
            return b
    '''


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #orig# parser.add_argument("--ip", default="0.0.0.0", type=str)
    #orig# parser.add_argument("--port", default=8080, type=int)
    #add
    parser.add_argument("--ip", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=8082, type=int)
    #
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LogCalculatorServicer()
    log_pb2_grpc.add_LogCalculatorServicer_to_server(servicer, server)
    
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(host='127.0.0.1', port=MQTT_PORT)
    client.subscribe('history', 0)



    try:
        #add
        client.loop_start()
        #
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        #orig# print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        print(f"Run log Server at {args['ip']}:{args['port']}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        #add
        client.loop_stop()
        #
        #orig# pass
