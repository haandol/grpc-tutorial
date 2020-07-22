import grpc

import todo_pb2
import todo_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:8080') as channel:
        stub = todo_pb2_grpc.TodoStub(channel)
        print(stub.createTodo(todo_pb2.TodoItem(id='id3', text='text3')))
        print(stub.createTodo(todo_pb2.TodoItem(id='id4', text='text4')))
        print(stub.createTodo(todo_pb2.TodoItem(id='id5', text='text5')))
        print(stub.createTodo(todo_pb2.TodoItem(id='id6', text='text6')))
        # print(stub.updateTodo(todo_pb2.TodoItem(id='id2', text='new new text2')))
        for todo in stub.listTodos((todo_pb2.Empty())):
            print(todo)


if __name__ == '__main__':
    run()
