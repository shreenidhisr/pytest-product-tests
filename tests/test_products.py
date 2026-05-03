import requests
import pytest

class TestProductDescription:
    def test_create_product_with_description(self, base_url, create_product):
        payload = {"name": "Gaming Mouse", "price": 50.0, "description": "High precision sensor"}
        product = create_product(payload)
        
        response = requests.get(f"{base_url}/products/{product['id']}")
        assert response.status_code == 200
        assert response.json()["description"] == "High precision sensor"

    def test_create_product_without_description(self, base_url, create_product):
        payload = {"name": "Basic Keyboard", "price": 20.0}
        product = create_product(payload)
        
        response = requests.get(f"{base_url}/products/{product['id']}")
        assert response.status_code == 200
        assert "description" not in response.json() or response.json()["description"] is None

    def test_update_product_description(self, base_url, create_product):
        product = create_product({"name": "Monitor", "price": 200.0})
        
        update_payload = {"name": "Monitor", "price": 200.0, "description": "4K Display"}
        response = requests.put(f"{base_url}/products/{product['id']}", json=update_payload)
        assert response.status_code == 200
        
        get_response = requests.get(f"{base_url}/products/{product['id']}")
        assert get_response.json()["description"] == "4K Display"