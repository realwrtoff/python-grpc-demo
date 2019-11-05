# python-grpc-demo
###Steps
1. write common.proto and hello.proto

2. generate proto code to rpc_package
    ```bash
    mkdir -p ./rpc_package
    python3 -m grpc_tools.protoc --proto_path=./protos --python_out=./rpc_package ./protos/common.proto
    python3 -m grpc_tools.protoc --proto_path=./protos --python_out=./rpc_package --grpc_python_out=./rpc_package ./protos/hello.proto
    ```

3. add the rpc_package path into the code, but I think it is not 666.

   edit hello_pb2.py: 

   ```pyt
   # import common_pb2 as common__pb2
   import rpc_package.common_pb2 as common__pb2
   ```

   edit hello_pb2_grpc.py: 

   ```pyt
   # import hello_pb2 as hello__pb2
   import rpc_package.hello_pb2 as hello__pb2
   ```

4. run grpc server 
    ```bash
    python3 grpc_server.py &
    ```

5. run grpc client
    ```bash
    python3 grpc_client.py
    ```

# python-grpc-demo with consul
###Steps
1. install consul or consul cluster
```bash
   wget https://releases.hashicorp.com/consul/1.6.1/consul_1.6.1_linux_amd64.zip
   unzip consul_1.6.1_linux_amd64.zip
   mv consul /usr/local/bin/
   # simple start
   # nohup consul &
   # start with params
   consul agent -server -bootstrap-expect=3 -data-dir=/data/consul -node=consul-dev -bind=192.168.1.125 -client=0.0.0.0 -datacenter=beijing -ui
```

2. run grpc consul server 
    ```bash
    python3 grpc_consul_server.py -c 192.168.1.125 &
    # you may run multi server with different port
    python3 grpc_consul_server.py -c 192.168.1.125 -p 9390
    python3 grpc_consul_server.py -c 192.168.1.125 -p 9391 
    # you can watch them in the consul server ui http://192.168.1.125:8500
    ```

3. run grpc consul client
    ```bash
    python3 grpc_consul_client.py  -c 192.168.1.125
    # run multi times, then you will find it request different ip port if there are multi servers.
    ```