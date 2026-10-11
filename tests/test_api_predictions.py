import pytest
from unittest.mock import patch

def test_predict_missing_candidate(client):
    r = client.get("/api/predictions/99999")
    assert r.status_code == 404
