from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

#add
import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../build/service/")
sys.path.insert(0, BUILD_DIR)

import json
import grpc
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

FIB_SERVER = '127.0.0.1:8081'
LOG_SERVER = '127.0.0.1:8082'
MQTT_PORT = 1883
#

# Create your views here.

'''orig
class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={ 'echo': 'hello world' }, status=200)
'''
#add

class FibView(APIView):
    permission_classes = (permissions.AllowAny,)
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(host='127.0.0.1', port=MQTT_PORT)
        self.client.loop_start()

    def post(self, request):
        decoded = request.body.decode('utf-8')
        body = json.loads(decoded)
        order = body['order']
        host = FIB_SERVER
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            request = fib_pb2.FibRequest()
            request.order = order

            response = stub.Compute(request)
            self.client.publish(topic='history', payload=order)
            return Response(data={ 'answer': response.value }, status=200)



class LogView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        '''
        decoded = request.body.decode('utf-8')
        body = json.loads(decoded)
        order = body['order']
        '''
        host = LOG_SERVER
        with grpc.insecure_channel(host) as channel:
            stub = log_pb2_grpc.LogCalculatorStub(channel)
            request = log_pb2.LogRequest()
            response = stub.Compute(request)
            return Response(data={ 'history': response.data[:] }, status=200)
#
