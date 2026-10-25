# 两个自定义异常类，各一两行：

# NotFoundError —— 表示"按 id 找东西没找到"

# DuplicateError —— 表示"要写入的东西和已有数据重复了"
class NotFoundError(Exception):
    def __init__(self, todo_id:int):
        self.todo_id = todo_id
        super().__init__(f"Todo {todo_id} not found")


class DuplicateError(Exception):
    def __init__(self, title:str):
        self.title = title
        super().__init__(f"{title} already exists")