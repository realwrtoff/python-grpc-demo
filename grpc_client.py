#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

import grpc
import json
from rpc_package.hello_pb2 import HelloRequest, BytesRequest
from rpc_package.hello_pb2_grpc import HelloWorldServiceStub


def async_data():
    info_dic = {
        'name': 'wangyi',
        'email': 'fmj_912',
        'time': 20191031
    }
    info_str = json.dumps(info_dic)
    info_byte = info_str.encode('utf-8')
    data = {
        'wc': b'realwrtoff',
        'qq': b'737858576',
        'fmj_912': info_byte
    }
    for k, v in data.items():
        req = BytesRequest()
        req.key = k
        req.value = v
        yield req


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', required=False, type=str, help="Specify host ip", default='127.0.0.1')
    parser.add_argument('-p', '--port', required=False, type=int, help="Specify grpc port", default=9380)
    args = parser.parse_args()

    # 连接 rpc 服务器
    ip_port = '{0}:{1}'.format(args.ip, args.port)
    channel = grpc.insecure_channel(ip_port)
    
    # 调用 rpc 服务
    stub = HelloWorldServiceStub(channel)
    request = HelloRequest()
    request.name = 'jim'
    response = stub.SayHello(request)
    print('Greeter client received: code=[{0}], msg=[{1}]'.format(response.code, response.message))
    request.name = 'realwrtoff'
    response = stub.SayHello(request)
    print('Greeter client received: code=[{0}], msg=[{1}]'.format(response.code, response.message))

    send_data = async_data()
    response = stub.Transfer(send_data)
    print('Greeter client received: code=[{0}], msg=[{1}]'.format(response.code, response.message))


if __name__ == '__main__':
    main()
