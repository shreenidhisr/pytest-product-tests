import requests
import pytest

class TestDescriptionField:
    def test_create_product_with_description(self, base_url, cleanup_products):
        payload = {"name": "Gaming Mouse", "price": 50.0, "description": "High precision sensor"}
        response = requests.post(f"{base_url}/products", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["description"] == "High precision sensor"

    def test_create_product_without_description(self, base_url, cleanup_products):
        payload = {"name": "Basic Keyboard", "price": 20.0}
        response = requests.post(f"{base_url}/products", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert "description" not in data or data["description"] is None

    def test_get_product_includes_description(self, base_url, create_product):
        product = create_product({"name": "Monitor", "price": 200.0, "description": "4K display"})
        response = requests.get(f"{base_url}/products/{product['id']}")
        assert response.status_code == 200
        assert response.json()["description"] == "4K display"

    def test_update_product_description(self, base_url, create_product):
        product = create_product({"name": "Desk", "price": 100.0, "description": "Old desk"})
        update_payload = {"name": "Desk", "price": 100.0, "description": "New standing desk"}
        response = requests.put(f"{base_url}/products/{product['id']}", json=update_payload)
        assert response.status_code == 200
        assert response.json()["description"] == "New standing desk"