def test_create_candidate(client):
    payload = {
        "external_id": "gh_1", "source": "linkedin", "role": "backend",
        "experience_years": 5, "skills_score": 85.0, "stage": "screen",
    }
    r = client.post("/api/candidates", json=payload)
    assert r.status_code == 201
    assert r.json()["external_id"] == "gh_1"

def test_create_duplicate(client):
    payload = {
        "external_id": "gh_2", "source": "x", "role": "y",
        "experience_years": 1, "skills_score": 50.0, "stage": "applied",
    }
    client.post("/api/candidates", json=payload)
    r = client.post("/api/candidates", json=payload)
    assert r.status_code == 409

def test_list_candidates(client):
    r = client.get("/api/candidates")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
