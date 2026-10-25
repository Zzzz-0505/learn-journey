#管HTTP
from app.exceptions import NotFoundError,DuplicateError





if __name__ == "__main__":
    res = str(NotFoundError(42))
    res2 = DuplicateError("打游戏")

    print(res)
