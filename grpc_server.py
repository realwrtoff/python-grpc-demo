#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time

from concurrent import futures
import grpc

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
        return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', required=False, type=str, help="Specify host ip", default='0.0.0.0')
    parser.add_argument('-p', '--port', required=False, type=int, help="Specify grpc port", default=9380)
    args = parser.parse_args()

    # 启动 rpc 服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_HelloWorldServiceServicer_to_server(Greeter(), server)
    server.add_insecure_port("{}:{}".format(args.ip, args.port))
    server.start()
    print('grpc server run at {}:{}'.format(args.ip, args.port))

    try:
        while True:
            time.sleep(60 * 60 * 24)  # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()
