import pytest
import requests
from unittest.mock import patch, Mock

class TestOrderUserIntegration:

    def test_user_order_valid_user_with_Service_integration(self, base_urls, semple_user, sample_items, skip_if_services_down):

        skip_if_services_down("user", "order")

        order_data = {
            "email": semple_user["email"],
            **sample_items
        }

        response = requests.post(f"{base_urls['order']}/create", json=order_data, allow_redirects=False)
        assert response.status_code == 302

    @patch('requests.post')
    def test_create_order_valid_user_mocked(self, mock_post, base_urls, semple_user, sample_items):
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {"Location": "/order/list"}
        mock_post.return_value = mock_response

        order_data = {
            "email": semple_user["email"], 
            **sample_items
        }

        response = requests.post(f"{base_urls['order']}/create", json=order_data, allow_redirects=False)
        assert response.status_code == 302

    def test_create_order_user_not_found_with_service(self, base_urls, sample_items, skip_if_services_down):
        skip_if_services_down("user", "order")

        order_data = {
            "email": "nonexistent@example.com",
            **sample_items
        }

        response = requests.post(f"{base_urls['order']}/create", json=order_data, allow_redirects=False)
        assert response.status_code in [404, 400]  # Depending on how the service handles not found users


    class TestServiceHealthCheck:
        def test_order_services_health_check(self, base_urls):
            try: 
                response = requests.get(f"{base_urls['order']}/", timeout=2)
                assert response.status_code in [200, 302, 404]
            except requests.exceptions.ConnectionError:
                pytest.skip("Order service is not running. Please ensure the service is up before running the tests.")


        def test_user_services_health_check(self, base_urls):
            try:
                response = requests.get(f"{base_urls['user']}/", timeout=2)
                assert response.status_code in [200, 302, 404]
            except requests.exceptions.ConnectionError:
                pytest.skip("User service is not running. Please ensure the service is up before running the tests.")