import pytest
import pandas as pd
import numpy as np
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks.task_manager import *

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Chemical': ['Meth', 'Acetone', 'Mercury'],
        'Amount': [25, 10, 0.5],
        'Unit': ['liter', 'liter', 'kg'],
        'IsHazardous': [True, False, True]
    })

def test_get_hazardous_chemicals(sample_df):
    result = get_hazardous_chemicals(sample_df)
    assert 'Meth' in result.values and 'Mercury' in result.values

def test_convert_amounts_to_grams(sample_df):
    df = convert_amounts_to_grams(sample_df)
    assert df['Amount'].tolist() == [25000, 10000, 500]

def test_get_top_n_chemicals(sample_df):
    df = convert_amounts_to_grams(sample_df)
    result = get_top_n_chemicals(df, 2)
    assert result.iloc[0]['Amount'] >= result.iloc[1]['Amount']

def test_get_unique_units(sample_df):
    units = get_unique_units(sample_df)
    assert set(units) == {'liter', 'kg'}

def test_filter_chemicals_by_name(sample_df):
    result = filter_chemicals_by_name(sample_df, "Acetone")
    assert result.iloc[0]['Chemical'] == "Acetone"

def test_get_total_amount(sample_df):
    df = convert_amounts_to_grams(sample_df)
    total = get_total_amount(df)
    assert total == 25000 + 10000 + 500

def test_calculate_standard_deviation(sample_df):
    df = convert_amounts_to_grams(sample_df)
    std = calculate_standard_deviation(df)
    assert isinstance(std, float)

def test_normalize_amounts(sample_df):
    df = convert_amounts_to_grams(sample_df)
    norm = normalize_amounts(df)
    assert np.isclose(norm.max(), 1.0)

def test_flag_high_risk(sample_df):
    df = convert_amounts_to_grams(sample_df)
    flagged = flag_high_risk(df)
    assert 'HighRisk' in flagged.columns

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")

class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://edugen-backend-487d2168bc6c.herokuapp.com/projectLog/"
    payload = {
        "user_id": 203,
        "project_id": 265,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()
