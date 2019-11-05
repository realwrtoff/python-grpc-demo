#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

import grpc
from dns import resolver
from dns.exception import DNSException

import json
import socket
from rpc_package.hello_pb2 import HelloRequest, BytesRequest
from rpc_package.hello_pb2_grpc import HelloWorldServiceStub


def get_lan_ip():
    return socket.gethostbyname(socket.getfqdn(socket.gethostname()))


def get_ip_port(consul_resolver, server_name):
    """查询出可用的一个ip，和端口"""
    try:
        key = '{0}.service.consul'.format(server_name)
        dnsanswer = consul_resolver.query(key, "A")
        dnsanswer_srv = consul_resolver.query(key, "SRV")
    except DNSException:
        return None, None
    return dnsanswer[0].address, dnsanswer_srv[0].port


def async_data():
    info_dic = {
        'name': 'wangyi',
        'email': 'fmj_912@163.com',
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
    parser.add_argument('-c', '--consul', required=False, type=str, help="Specify consul host ip", default=get_lan_ip())
    parser.add_argument('-i', '--ip', required=False, type=str, help="Specify host ip", default=get_lan_ip())
    parser.add_argument('-p', '--port', required=False, type=int, help="Specify grpc port", default=9380)
    args = parser.parse_args()

    # 连接consul服务，作为dns服务器
    consul_resolver = resolver.Resolver()
    consul_resolver.port = 8600
    consul_resolver.nameservers = [args.consul]

    # 查询服务对应的ip和port
    service_name = 'grpc_trans_server'
    ip, port = get_ip_port(consul_resolver, service_name)
    if ip is None:
        ip_port = '{0}:{1}'.format(args.ip, args.port)
    else:
        ip_port = '{0}:{1}'.format(ip, port)
    print(ip_port)

    # 连接 rpc 服务器
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
