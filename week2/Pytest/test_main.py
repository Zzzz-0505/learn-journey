from main import get_weather,add,divide,UserManager,Database,is_prime,get_weather_api,UserService,APIClient
import pytest

# def test_get_weather():
#     assert get_weather(21) == "hot"
#------------------------------------------------

# def test_add():
#     assert add(2,3) == 5,"2 + 3 should be 5"
#     assert add(-1,1) == 0,"-1 + 1 should be 0"
#     assert add(0,0) == 1, "0 + 0 should be 0"

# def test_divide():
#     with pytest.raises(ValueError,match="Cannot divide by zero"):
#         divide(10,0)

#------------------------------------------------


# @pytest.fixture
# def user_manager():
#     """Creates a fresh instance of UserManager before each test."""
#     return UserManager()

# def test_add_user(user_manager):
#     assert user_manager.add_user("john_doe","john@example.com") == True
#     assert user_manager.get_user("john_doe") == "john@example.com"

# def test_add_duplicate_user(user_manager):
#     user_manager.add_user("john_doe","john@example.com")
#     with pytest.raises(ValueError):
#         user_manager.add_user("john_doe","another@example.com")


#------------------------------------------------

#数据库测试
# @pytest.fixture
# def database():
#     database = Database()
#     yield database # Provice the fixture instance
#     database.data.clear() # Clean up step(not needed for in-memory,but useful for real DBs)


# def test_add_user(database):
#     database.add_user(1,"zhangsan")
#     assert database.get_user(1) == "zhangsan"

# def test_add_duplicate_user(database):
#     database.add_user(1,"zhangsan")
#     with pytest.raises(ValueError,match="User already exist"):
#         database.add_user(1,"Bob")

# def test_delete_user(database):
#     database.add_user(2,"Bob")
#     database.delete_user(2)
#     database.get_user(2) is None
#------------------------------------------------

#参数化测试-当需要输入很多个参数，但重复性很高可以考虑使用参数列表
# @pytest.mark.parametrize("num,expected",[
#     (1,False),
#     (2,True),
#     (3,True),
#     (4,False),
#     (5,True),
#     (6,False),
#     (7,True),

# ])
# def test_is_prime(num,expected):
#     assert is_prime(num) == expected

#------------------------------------------------

#mocks
# def test_get_weather_api(mocker):
#     #Mock requests.get
#     mock_get = mocker.patch("main.requests.get")

#     #Set return values
#     mock_get.return_value.status_code = 200
#     mock_get.return_value.json.return_value = {"temperature":25,"condition":"Sunny"}

#     #Call function
#     result = get_weather_api("beijing")

#     #Assertions
#     assert result == {"temperature":25,"condition":"Sunny"}
#     mock_get.assert_called_once_with("https://api.weather.com/v1/beijing") 


#------------------------------------------------
def test_get_username_with_mock(mocker):
    mock_api_client = mocker.Mock(spec=APIClient) #Create a mock API client

    # Mock get_user_data to return a fake user
    mock_api_client.get_user_data.return_value = {"id":1,"name":"Alice"}

    service = UserService(mock_api_client) # Inject mock API client

    result = service.get_username(1) # Call method that depends on the mock
    # Assertions
    assert result == "Alice"    # Check if processing was done correctly
    mock_api_client.get_user_data.assert_called_once_with(1) #Ensure correct API call