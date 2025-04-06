import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from src.data_processing.cleaner import BostonHousingCleaner


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'CRIM': [0.1, 0.2, np.nan, 0.4],
        'MEDV': [30, 50, 1000, 40],
        'CHAS': [0, 1, 0, 0]
    })

def test_missing_values(sample_data):
    cleaner = BostonHousingCleaner("dummy.csv", "dummy_out.csv")
    cleaner.df = sample_data.copy()
    cleaner.handle_missing_values()
    assert not cleaner.df.isnull().any().any()

def test_outlier_removal(sample_data):
    cleaner = BostonHousingCleaner("dummy.csv", "dummy_out.csv")
    cleaner.df = sample_data.copy()
    cleaner.remove_outliers('MEDV')
    assert len(cleaner.df) < len(sample_data)

@patch('pandas.read_csv')
def test_integration(mock_read, sample_data, tmp_path):
    mock_read.return_value = sample_data
    output_path = tmp_path / "clean.csv"
    cleaner = BostonHousingCleaner("dummy.csv", output_path)
    result = cleaner.run_pipeline()
    assert isinstance(result, pd.DataFrame)
    assert output_path.exists()