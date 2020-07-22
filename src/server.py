import json
import grpc
from concurrent import futures

import todo_pb2
import todo_pb2_grpc


class DB(object):
    def __init__(self):
        self.data = self.load()

    def load(self):
        with open('db.json', 'r') as fp:
            s = fp.read()
            return json.loads(s)

    def create(self, todo):
        if todo.id in self.data:
            raise RuntimeError(f'{todo.id} already exists')

        self.data[todo.id] = todo.text
        return todo

    def get(self, req):
        if req.id not in self.data:
            raise RuntimeError(f'{req.id} does not exists')

        return todo_pb2.TodoItem(id=req.id, text=self.data[req.id])

    def delete(self, req):
        if req.id not in self.data:
            raise RuntimeError(f'{req.id} does not exists')

        del self.data[req.id]
        return todo_pb2.Empty()

    def update(self, todo):
        if todo.id not in self.data:
            raise RuntimeError(f'{todo.id} does not exists')

        self.data[todo.id] = todo.text
        return todo

    def list_todo(self):
        return todo_pb2.TodoItems(items=[
            todo_pb2.TodoItem(id=id, text=text)
            for id, text in self.data.items()
        ])

    def save(self):
        with open('db.json', 'w') as fp:
            fp.write(json.dumps(self.data))
        return todo_pb2.Empty()


class TodoServicer(todo_pb2_grpc.TodoServicer):
    def __init__(self):
        self._db = DB()

    @property
    def db(self):
        return self._db

    def createTodo(self, request, context):
        return self.db.create(request)

    def getTodo(self, request, context):
        return self.db.get(request)

    def updateTodo(self, request, context):
        return self.db.update(request)

    def deleteTodo(self, request, context):
        return self.db.delete(request)

    def listTodos(self):
        return self.db.list_todo()

    def save(self, request, context):
        return self.db.save()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    todo_pb2_grpc.add_TodoServicer_to_server(TodoServicer(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()