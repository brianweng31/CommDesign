from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../build/service/")
sys.path.insert(0, BUILD_DIR)

import json
import grpc
import fib_pb2
import fib_pb2_grpc


import paho.mqtt.client as mqtt

LOCALHOST = "127.0.0.4"
FIB_SERVER = "127.0.0.1:8081"
LOG_SERVER = "127.0.0.1:8082"
DOCKER_PORT = 1883

# Create your views here.
        
        
## publisher
class FibView(APIView):
	permission_classes = (permissions.AllowAny,)
    
	def __init__(self):
		self.client = mqtt.Client()
		self.client.connect(host=LOCALHOST, port=DOCKER_PORT)
		#self.client.loop_start()
		
	def post(self, request):
		decoded = request.body.decode('utf-8')
		body = json.loads(decoded)
		data = body['order']
		host = FIB_SERVER
		with grpc.insecure_channel(host) as channel:
			stub = fib_pb2_grpc.FibCalculatorStub(channel)

			request = fib_pb2.FibRequest()
			order = int(data)
			request.order = order 
			response = stub.Compute(request)

			self.client.publish(topic='his', payload=order)
			return Response(data={ 'success': True, 'data': response.value }, status=200)


class LogView(APIView):
	permission_classes = (permissions.AllowAny,)
    
    	
	def get(self, request):
		host = LOG_SERVER		
		with grpc.insecure_channel(host) as channel:
			stub = log_pb2_grpc.LogStub(channel)
			request = log_pb2.LogRequest()
			response = stub.Get(request)
			print("Response data,", response.data)
			return Response(data={'success' : True, 'history' : response.data[:]}, status=200)
