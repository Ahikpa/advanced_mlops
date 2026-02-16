import pytest
from fastapi.testclient import TestClient
import unittest.mock as mock
import os
import sys

# Add the project root to sys.path to allow importing from 'api'
sys.path.append(os.path.join(os.getcwd(), 'api'))

from main import app

client = TestClient(app)

def test_health_check():
    """Verify that the API health check endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_reload_endpoint_mocked():
    """Verify that the /reload endpoint triggers correctly (with mocked model loading)."""
    with mock.patch("main.load_latest_model") as mock_load:
        response = client.post("/reload")
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        mock_load.assert_called_once()

def test_predict_without_model():
    """Verify that prediction fails gracefully if no model is loaded."""
    # We force the global 'model' to None for this test
    with mock.patch("main.model", None):
        with mock.patch("main.load_latest_model") as mock_load:
            # Mocking load_latest_model to stay None
            response = client.post("/predict", json={
                "Age": 33, "Sex": "male", "Job": 2, "Housing": "own",
                "Saving_accounts": "little", "Checking_account": "moderate",
                "Credit_amount": 2500, "Duration": 12, "Purpose": "car"
            })
            assert response.status_code == 503
            assert "Model not loaded" in response.json()["detail"]
