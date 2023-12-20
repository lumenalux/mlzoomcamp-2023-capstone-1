import requests
import json

def test_model(url, endpoint, data):
    response = requests.post(f"{url}/predict/{endpoint}", json=data)
    print(f"Response from {endpoint}: {response.json()}")


if __name__ == '__main__':
  URL = "http://localhost:5000"

  data = {
      "CNT_CHILDREN": 2,
      "AMT_INCOME_TOTAL": 50000,
      "AMT_CREDIT": 200000,
      "AMT_ANNUITY": 10000,
      "AMT_GOODS_PRICE": 180000,
      "REGION_POPULATION_RELATIVE": 0.01,
      "DAYS_BIRTH": -12000,
      "DAYS_EMPLOYED": -2000,
      "DAYS_REGISTRATION": -3000,
      "DAYS_ID_PUBLISH": -1500,
      "FLAG_WORK_PHONE": 1,
      "REGION_RATING_CLIENT": 2,
      "HOUR_APPR_PROCESS_START": 10
  }

  # Test each models endpoint
  test_model(URL, "logistic_regression", data)
  test_model(URL, "random_forest", data)
  test_model(URL, "xgboost", data)
