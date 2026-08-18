from pathlib import Path

import pandas as pd
import pytest

from src.analyze import load_data, summarize


def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "season": [1, 1], "year": [0, 0], "hour": [8, 17],
            "holiday": [0, 0], "weekday": [1, 1], "weathersit": [1, 2],
            "temp": [0.3, 0.4], "humidity": [0.5, 0.6], "windspeed": [0.1, 0.2],
            "bikes_per_hour": [100, 200],
        }
    )


def test_summary_identifies_peak_hour() -> None:
    result = summarize(sample_frame())
    assert result["records"] == 2
    assert result["total_rides"] == 300
    assert result["peak_hour"] == 17


def test_load_data_rejects_missing_columns(tmp_path: Path) -> None:
    path = tmp_path / "bad.csv"
    pd.DataFrame({"hour": [1]}).to_csv(path, index=False)
    with pytest.raises(ValueError, match="Missing required columns"):
        load_data(path)
