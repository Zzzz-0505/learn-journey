#管数据
from schemas import TodoCreate,TodoOut
from exceptions import NotFoundError,DuplicateError

class TodoRepository():#它代表货架，不代表货
    def __init__(self):
        self._store = dict[int,TodoOut] = {}
        self._next_id = 1

    def create(self,data:TodoCreate) -> TodoOut:
        for t in self._store.values():
            if data.title == t.title: 
                raise DuplicateError(data.title)
        res = TodoOut.model_validate({**data.model_dump(), "id": self._next_id})
        self._store[res.id] = res
        self._next_id += 1
        return res

    def get(self,todo_id:int) -> TodoOut:
        if todo_id  in self._store:return self._store[todo_id]
        raise NotFoundError(todo_id)

    def list_all(self,limit:int) ->list[TodoOut]:
        return list(self._store.values())[:limit]

    def delete(self,todo_id:int)->None:
        if todo_id not in self._store:raise NotFoundError(todo_id)
        del self._store[todo_id]
        

    def update(self,todo_id:int,data:TodoCreate) -> TodoOut:
        if todo_id not in self._store:raise NotFoundError(todo_id)
        for t in self._store.values():
            if t.title == data.title and t.id != todo_id:
                raise DuplicateError(data.title)
        res = TodoOut.model_validate({**data.model_dump(), "id": todo_id})
        self._store[todo_id] = res
        return res
