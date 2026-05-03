"""
Existing hand-written system tests for the Product API.
These serve as examples for the AI to follow when generating new tests.
"""
import requests
import pytest


class TestGetProducts:
    def test_get_all_products_returns_list(self, base_url):
        response = requests.get(f"{base_url}/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_product_by_id(self, base_url, create_product):
        product = create_product({"name": "Laptop", "price": 999.99})
        response = requests.get(f"{base_url}/products/{product['id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product["id"]
        assert data["name"] == "Laptop"
        assert data["price"] == 999.99

    def test_get_nonexistent_product_returns_404(self, base_url):
        response = requests.get(f"{base_url}/products/999999")
        assert response.status_code == 404


class TestCreateProduct:
    def test_create_product_returns_201(self, base_url, create_product):
        product = create_product({"name": "Mouse", "price": 29.99})
        assert product["id"] is not None
        assert product["name"] == "Mouse"
        assert product["price"] == 29.99

    def test_create_product_missing_name_returns_400(self, base_url):
        response = requests.post(f"{base_url}/products", json={"price": 10.0})
        assert response.status_code == 400

    def test_create_product_missing_price_returns_400(self, base_url):
        response = requests.post(f"{base_url}/products", json={"name": "Keyboard"})
        assert response.status_code == 400

    def test_create_product_negative_price_returns_400(self, base_url):
        response = requests.post(f"{base_url}/products", json={"name": "Keyboard", "price": -5.0})
        assert response.status_code == 400


class TestUpdateProduct:
    def test_update_product_returns_200(self, base_url, create_product):
        product = create_product({"name": "Tablet", "price": 499.99})
        response = requests.put(
            f"{base_url}/products/{product['id']}",
            json={"name": "Tablet Pro", "price": 599.99}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Tablet Pro"
        assert data["price"] == 599.99

    def test_update_nonexistent_product_returns_404(self, base_url):
        response = requests.put(
            f"{base_url}/products/999999",
            json={"name": "Ghost", "price": 1.0}
        )
        assert response.status_code == 404


class TestDeleteProduct:
    def test_delete_product_returns_204(self, base_url, create_product):
        product = create_product({"name": "Headphones", "price": 79.99})
        response = requests.delete(f"{base_url}/products/{product['id']}")
        assert response.status_code == 204

    def test_delete_product_removes_it(self, base_url, create_product):
        product = create_product({"name": "Monitor", "price": 349.99})
        requests.delete(f"{base_url}/products/{product['id']}")
        get_response = requests.get(f"{base_url}/products/{product['id']}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_product_returns_404(self, base_url):
        response = requests.delete(f"{base_url}/products/999999")
        assert response.status_code == 404
