# python-grpc-demo
###Steps
1. write common.proto and hello.proto

2. generate proto code to rpc_package
    ```bash
    python3 -m grpc_tools.protoc --proto_path=./protos --python_out=./rpc_package ./protos/common.proto
    python3 -m grpc_tools.protoc --proto_path=./protos --python_out=./rpc_package --grpc_python_out=./rpc_package ./protos/hello.proto
    ```

3. add the rpc_package path into the code, but I think it is not 666.

   edit hello_pb2.py: 

   ```pyt
   import rpc_package.common_pb2 as common__pb2
   ```

   edit hello_pb2_grpc.py: 

   ```pyt
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

