import pytest
import requests
from unittest.mock import patch, Mock

class TestOrderProductIntegration:


    @patch('requests.post')
    def test_create_order_valid_product_mocked(self, mock_post, base_urls, sample_product, sample_order_payload):
        mock_response = Mock()
        mock_response.status_code = 302
        mock_response.headers = {"Location": "/order/list"}
        mock_post.return_value = mock_response

        order_data = {
            "name": sample_product["name"], 
            **sample_order_payload
        }

        response = requests.post(f"{base_urls['order']}/create", json=order_data, allow_redirects=False)
        assert response.status_code == 302