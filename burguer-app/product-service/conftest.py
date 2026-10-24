import pytest
import requests
from unittest.mock import patch, Mock
from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv


@pytest.fixture()
def base_urls():
    return {
        "auth_url": "http://localhost:5000/auth",
        "user": "http://localhost:5001/user",
        "order": "http://localhost:5002/order",
        "product_url": "http://localhost:5003/product"
    }



@pytest.fixture 
def sample_product(): 
    """Produto válido para cadastro.""" 
    return { 
        "name": "X-Burger", 
        "description": "Hambúrguer artesanal com queijo", 
        "category": "Lanche", 
        "price": 25.00, 
        "available": True, 
        "ingredients": ["pão", "carne", "queijo", "alface", "molho"] 
    } 


@pytest.fixture 
def sample_order_payload(): 
    """Payload básico para criar pedido.""" 
    # O produto será inserido dinamicamente no teste 
    return {
        "items": ["Cachorro quente", "Hamburger"]
    } 