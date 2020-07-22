import grpc

import todo_pb2
import todo_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = todo_pb2_grpc.TodoStub(channel)
        print(stub.createTodo(todo_pb2.TodoItem(id='id2', text='text2')))
        print(stub.updateTodo(todo_pb2.TodoItem(id='id2', text='new new text2')))
        print(stub.getTodo(todo_pb2.RequestId(id='id2')))
        print(stub.save(todo_pb2.Empty()))


if __name__ == '__main__':
    run()
