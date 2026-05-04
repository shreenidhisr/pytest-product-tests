import pytest
import requests

class TestProductDescription:
    def test_create_product_with_description_and_company(self, base_url, create_product):
        payload = {
            "name": "Mechanical Keyboard",
            "price": 99.99,
            "description": "High quality switches",
            "company": "TechCorp"
        }
        product = create_product(payload)
        assert product["description"] == "High quality switches"
        assert product["company"] == "TechCorp"

    def test_create_product_without_optional_fields(self, base_url, create_product):
        payload = {"name": "Mouse", "price": 25.0}
        product = create_product(payload)
        assert "description" not in product or product["description"] is None
        assert "company" not in product or product["company"] is None

    def test_update_product_description_and_company(self, base_url, create_product):
        product = create_product({"name": "Monitor", "price": 200.0})
        update_payload = {
            "name": "Monitor",
            "price": 200.0,
            "description": "4K Display",
            "company": "DisplayCo"
        }
        response = requests.put(f"{base_url}/products/{product['id']}", json=update_payload)
        assert response.status_code == 200
        updated = response.json()
        assert updated["description"] == "4K Display"
        assert updated["company"] == "DisplayCo"

class TestCreateProduct:
    def test_create_product_negative_price_returns_400(self, base_url):
        response = requests.post(f"{base_url}/products", json={"name": "Keyboard", "price": -5.0})
        assert response.status_code == 400

    def test_create_product_missing_name_returns_400(self, base_url):
        response = requests.post(f"{base_url}/products", json={"price": 10.0})
        assert response.status_code == 400

    def test_create_product_missing_price_returns_400(self, base_url):
        response = requests.post(f"{base_url}/products", json={"name": "Keyboard"})
        assert response.status_code == 400

class TestGetProducts:
    def test_get_all_products_returns_list(self, base_url):
        response = requests.get(f"{base_url}/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)