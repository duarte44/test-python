import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.user_model import UserModel


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.user_data = UserModel(
            email="teste@exemplo.com",
            name="Teste",
            address="123 Test St",
            role="cliente"
        )

    def tearDown(self):
        self.user_data = None

    def test_to_dict(self):
        expected_dict = {
            "email": "teste@exemplo.com",
            "name": "Teste",
            "address": "123 Test St",
            "role": "cliente"
        }
        self.assertEqual(self.user_data.to_dict(), expected_dict)

    def test_serialize_user_incomplete(self):
        result = self.user_data.serialize()
        self.assertEqual(result["email"], "teste@exemplo.com")
        self.assertEqual(result["name"], "Teste")
        self.assertNotIn("password", result)

    def test_assert_raises_example(self):
        def raise_error():
            raise ValueError("This is a test error")

        with self.assertRaises(ValueError):
            raise_error()
