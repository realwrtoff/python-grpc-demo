#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time

from concurrent import futures
import grpc
import consul
import socket

from rpc_package.common_pb2 import ErrorCode
from rpc_package.hello_pb2 import HelloReply
from rpc_package.hello_pb2_grpc import HelloWorldServiceServicer, add_HelloWorldServiceServicer_to_server


class Greeter(HelloWorldServiceServicer):
    def SayHello(self, request, context):
        response = HelloReply()
        if request.name == 'jim':
            response.code = ErrorCode.FAIL
            response.message = 'You are in the black list!'
        else:
            response.code = ErrorCode.OK
            response.message = f'Hello {request.name}'
        print('unary call : name = {0}'.format(request.name))
        return response

    def Transfer(self, request_iterator, context):
        response = HelloReply()
        num = 0
        for request in request_iterator:
            num += 1
            if type(request.value) is bytes:
                value = request.value.decode('utf-8')
            else:
                value = request.value
            print('stream[{0}]: {1} = {2}'.format(num, request.key, value))
        response.code = ErrorCode.OK
        response.message = 'stream receive {0} message'.format(num)
        return response


def register(c, server_name, ip, port):
    check = consul.Check.tcp(ip, port, "10s")  # 健康检查的ip，端口，检查时间
    c.agent.service.register(server_name, f"{server_name}-{ip}-{port}",
                             address=ip, port=port, check=check)  # 注册服务部分
    print(f"注册服务{server_name}成功")


def unregister(c, server_name, ip, port):
    print(f"开始退出服务{server_name}")
    c.agent.service.deregister(f'{server_name}-{ip}-{port}')


def get_lan_ip():
    return socket.gethostbyname(socket.getfqdn(socket.gethostname()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--consul', required=False, type=str, help="Specify consul host ip", default=get_lan_ip())
    parser.add_argument('-i', '--ip', required=False, type=str, help="Specify host ip", default=get_lan_ip())
    parser.add_argument('-p', '--port', required=False, type=int, help="Specify grpc port", default=9380)
    args = parser.parse_args()

    # 启动rpc服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HelloWorldServiceServicer_to_server(Greeter(), server)
    server.add_insecure_port("{}:{}".format(args.ip, args.port))

    # 注册consul
    c = consul.Consul(args.consul)
    service_name = 'grpc_trans_server'
    register(c, service_name, args.ip, args.port)

    server.start()
    print('grpc server run at {}:{}'.format(args.ip, args.port))

    try:
        while True:
            time.sleep(60 * 60 * 24)  # one day in seconds
    except KeyboardInterrupt:
        unregister(c, service_name, args.ip, args.port)
        print('exception killed')
        server.stop(0)


if __name__ == '__main__':
    main()
