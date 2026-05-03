import os
import pytest
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:8080")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(autouse=True)
def cleanup_products(base_url):
    """Delete all products created during a test by tracking IDs."""
    created_ids = []
    yield created_ids
    for product_id in created_ids:
        requests.delete(f"{base_url}/products/{product_id}")


@pytest.fixture
def create_product(base_url, cleanup_products):
    """Helper fixture to create a product and auto-register it for cleanup."""
    def _create(payload):
        response = requests.post(f"{base_url}/products", json=payload)
        assert response.status_code == 201
        data = response.json()
        cleanup_products.append(data["id"])
        return data
    return _create
