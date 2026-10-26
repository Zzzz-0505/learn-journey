#测行为  关心repository 业务行为对不对
import pytest
from app.repository import TodoRepository
from app.schemas import TodoCreate
from app.exceptions import NotFoundError,DuplicateError
from datetime import date

@pytest.fixture
def repo():
    return TodoRepository()

@pytest.fixture
def repo_with_data(repo):
    data1 = TodoCreate(title="a",deadline=date(2024,1,1),level=2)
    data2 = TodoCreate(title="b",deadline=date(2024,1,1),level=2)
    data3 = TodoCreate(title="c",deadline=date(2024,1,1),level=2)
    repo.create(data=data1)
    repo.create(data=data2)
    repo.create(data=data3)
    return repo

def test_create_returns_todo_with_id(repo):
    data = TodoCreate(title="x",deadline=date(2024,1,1),level=2)
    res = repo.create(data=data)
    assert res.id == 1
    assert res.title == "x"
    assert res.level == 2

def test_create_increments_id(repo):
    data1 = TodoCreate(title="a",deadline=date(2024,1,1),level=2)
    data2 = TodoCreate(title="b",deadline=date(2024,1,1),level=2)
    res1 = repo.create(data=data1)
    res2 = repo.create(data=data2)
    assert res1.id == 1
    assert res2.id == 2

def test_get_returns_created(repo):
    data = TodoCreate(title="x",deadline=date(2024,1,1),level=2)
    res1 = repo.create(data=data)
    res2 = repo.get(res1.id)
    assert res1 == res2

def test_list_all_empty_returns_empty_list(repo):
    assert repo.list_all(10) == []

def test_list_all_respects_limit(repo):
    data1 = TodoCreate(title="a",deadline=date(2024,1,1),level=2)
    data2 = TodoCreate(title="b",deadline=date(2024,1,1),level=2)
    data3 = TodoCreate(title="c",deadline=date(2024,1,1),level=2)
    repo.create(data=data1)
    repo.create(data=data2)
    repo.create(data=data3)
    length = len(repo.list_all(2))
    assert length == 2

def test_get_not_found(repo):
    with pytest.raises(NotFoundError)as exc_info:
        repo.get(999)
    assert exc_info.value.todo_id == 999

def test_update_not_found(repo):
    data1 = TodoCreate(title="a",deadline=date(2024,1,1),level=2)
    repo.create(data=data1)
    new_data = TodoCreate(title="right data",deadline=date(2024,1,1),level=2)
    with pytest.raises(NotFoundError):
        repo.update(999,data=new_data)

def test_delete_not_found(repo):
    with pytest.raises(NotFoundError):
        repo.delete(999)

def test_create_duplicate_title(repo_with_data):
    data = TodoCreate(title="a",deadline=date(2024,1,1),level=3)
    with pytest.raises(DuplicateError):
        repo_with_data.create(data)

def test_update_to_others_title(repo_with_data):
    new_data = TodoCreate(title="b",deadline=date(2024,1,1),level=2)
    with pytest.raises(DuplicateError):
        repo_with_data.update(1,data=new_data)

def test_update_same_title_no_error(repo_with_data):
    new_data = TodoCreate(title="a",deadline=date(2024,1,1),level=3)
    res = repo_with_data.update(1,data=new_data)
    assert res.title == "a"
    assert res.level == 3


