import pytest
import requests
from unittest.mock import patch, Mock
from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# load_dotenv()

# @pytest.fixture(scope="session")
# def mongo_client():
#     uri = os.getenv("MONGO_URI")
#     client = MongoClient(uri)
#     yield client
#     client.close()

# @pytest.fixture(scope="function")
# def test_db(mongo_client):
#     db = mongo_client["burguer_app_test"]

#     db["users"].delete_many({})  # Limpa a coleção de usuários antes de cada teste
#     db["pedidos"].delete_many({})  # Limpa a coleção de pedidos antes de cada teste
   
#     yield db



@pytest.fixture()
def base_urls():
    return {
        "auth_url": "http://localhost:5000/auth",
        "user": "http://localhost:5001/user",
        "order": "http://localhost:5002/order",
        "product_url": "http://localhost:5003/product"
    }

@pytest.fixture()
def semple_user():
    return {
        "email": "testuser@example.com",
        "password": "testpassword",
        "name": "Test User",
        "address": "123 Test St",
        "role": "cliente"
    }

@pytest.fixture()
def sample_items():
    return {
            "iten_name": ["Hambuerguer teste", "refrigerante teste"],
            "item_price": ["10.00", "5.00"],
            "quantity": ["1", "2"]
    }

@pytest.fixture()
def mock_user_service():
    with patch(requests.get) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "name": "Test User",
            "address": "123 Test St",
            "role": "cliente"
        }
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture()
def mock_order_service():
    with patch(requests.get) as mock_get:
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.headers = {"Location": "/order/list"}
        mock_get.return_value = mock_response
        yield mock_get


def check_service_health(url):
    try:
        response = requests.get(f"{url}/", timeout=2)
        return response.status_code in [200, 302, 404]
    except requests.exceptions.ConnectionError:
        return False

@pytest.fixture
def services_running(base_urls):
   return {
       service: check_service_health(url)
       for service, url in base_urls.items()

   }

@pytest.fixture
def skip_if_services_down(services_running):
    def _skip_if_down(*required_services):
        for service in required_services:
            if not services_running.get(f"{service}_url", False):
                pytest.skip(f"{service} is not running.")
    return _skip_if_down