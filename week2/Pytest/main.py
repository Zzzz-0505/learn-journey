def get_weather(temp):
    if temp >20:
        return "hot"
    else:
        return "cold"
#------------------------------------------------
 
def add(a,b):
    return a+b

def divide(a,b):
    if b == 0:
        raise ValueError("Caanot divide by zero")
    else:
        return a/b
#------------------------------------------------


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self,username,email):
        if username in self.users:
            raise ValueError("User already exists")
        self.users[username] = email
        return True

    def get_user(self,username):
        return self.users.get(username)

#------------------------------------------------


class Database:
    """Simulates a basic user database"""
    def __init__(self):
        self.data = {} #Simulating am im-memory darabase

    def add_user(self,user_id,name):
        if user_id in self.data:
            raise ValueError("User already exists")
        self.data[user_id] = name

    def get_user(self,user_id):
        return self.data.get(user_id,None)

    def delete_user(self,user_id):
        if user_id in self.data:
            del self.data[user_id]

#------------------------------------------------


def is_prime(n):
    if n < 2:
        return False
    for i in range(2,int(n **0.5)+1):
        if n % i ==0:
            return False
    return True

#------------------------------------------------

#mocks（模拟依赖项的虚拟版本）
import requests

def get_weather_api(city):
    res = requests.get(f"https://api.weather.com/v1/{city}")
    if res.status_code == 200:
        return res.json()
    else:
        raise ValueError("Could not fetch weather data")

#----------------------------------------------

class APIClient:
    """Simulates an external API client"""
    def get_user_data(self,user_id):
        response =requests.get(f"https://api.example.com/users/{user_id}")
        if response.status_code == 200:
            return response.josn()
        raise ValueError("API request failed")

class UserService:
    """Uses APIClient to fetch user data and process it."""
    def __init__(self,api_client):
        self.api_client = api_client    # Dependency injection

    def get_username(self,user_id):
        """Fetches a user and retuens their username in uppercase."""
        user_data = self.api_client.get_user_data(user_id)  #Calls API client
        return user_data["name"].upper()    #Processes the result
        