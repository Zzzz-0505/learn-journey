#测规则  关心pydantic 校验规则对不对

from app.schemas import TodoCreate,TodoOut
import pytest
from datetime import date
from pydantic import ValidationError


def test_Todo_create_ok():
    todo = TodoCreate(title="a", deadline=date(2024,1,1), level=1)
    assert todo.title == "a"
    assert todo.level == 1


def test_title_lose():
    with pytest.raises(ValidationError):
        TodoCreate(deadline=date(2024,1,1), level=1)

def test_title_empty():
    with pytest.raises(ValidationError):
        TodoCreate(title="",deadline=date(2024,1,1),level=1)

def test_title_over():
    with pytest.raises(ValidationError):
        TodoCreate(title="x"*21,deadline=date(2024,1,1),level=1)

def test_title_edge():
    todo = TodoCreate(title="x"*20,deadline=date(2024,1,1),level=1)
    assert todo.title == "x"*20

def test_title_1():
    assert TodoCreate(title="x",deadline=date(2024,1,1),level=1)

def test_deadline_lost():
    with pytest.raises(ValidationError):
        TodoCreate(title="123",level=1)

def test_deadline_format1():
    with pytest.raises(ValidationError):
        TodoCreate(title="123",deadline="abc",level=1)

def test_deadline_format2():
    with pytest.raises(ValidationError):
        TodoCreate(title="123",deadline="2024-02-30",level=1)

def test_level_format1():
    with pytest.raises(ValidationError):
        TodoCreate(title="123",deadline=date(2024,1,1),level=4)

def test_level_format2():
    with pytest.raises(ValidationError):
        TodoCreate(title="123",deadline=date(2024,1,1),level=0)

def test_level_format3():
    with pytest.raises(ValidationError):
        TodoCreate(title="123",deadline=date(2024,1,1),level=1.5)

def test_level_format4():
    with pytest.raises(ValidationError):
        TodoCreate(title="123",deadline=date(2024,1,1),level="1")

def test_more_parameter():
        todo =  TodoCreate(id=99,title="123",deadline=date(2024,1,1),level=3)
        assert "id" not in todo.model_dump() 

def test_TodoOut():
    out = TodoOut(id=1,title="a", deadline=date(2024,1,1), level=1)
    assert out.id == 1
    assert out.title == "a"
    assert out.level == 1


def test_todo_out_does_not_validate():
    todo =  TodoOut(id=2,title="",deadline=date(2024,1,1),level=2)
    assert todo.title == ""
    assert todo.id == 2