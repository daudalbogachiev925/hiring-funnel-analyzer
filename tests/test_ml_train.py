import pandas as pd
import pytest
from app.ml.train import train

@pytest.fixture
def sample_df(tmp_path):
    data = {
        "experience_years": [1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10],
        "skills_score": [50,55,60,65,70,75,80,85,90,95]*2,
        "source": ["a","b"]*10,
        "role": ["r1","r2"]*10,
        "stage": ["screen","tech"]*10,
        "offered": [0,0,0,1,0,1,1,1,1,1]*2,
    }
    return pd.DataFrame(data)

def test_train_pipeline(sample_df, tmp_path):
    out = tmp_path / "model.pkl"
    metrics = train(sample_df, str(out))
    assert out.exists()
    assert 0.0 <= metrics["test_auc"] <= 1.0
    assert metrics["n_samples"] == 20
