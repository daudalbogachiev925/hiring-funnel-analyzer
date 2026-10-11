import pandas as pd
from app.ml.features import candidate_to_frame
from app.models import Candidate

def test_candidate_to_frame():
    c = Candidate(id=1, external_id="x", source="a", role="b",
                  experience_years=3, skills_score=70.0, stage="tech")
    df = candidate_to_frame(c)
    assert isinstance(df, pd.DataFrame)
    assert df.iloc[0]["experience_years"] == 3
    assert "stage" in df.columns
