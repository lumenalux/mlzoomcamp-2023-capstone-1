import os
import pandas as pd

import joblib
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

RANDOM_STATE = 42

def load_and_preprocess_data():
    df = pd.read_csv('dataset/credit-evaluation.csv')
    imputer = SimpleImputer(strategy='median')
    df[df.columns] = imputer.fit_transform(df)

    X = df.drop(['TARGET', 'id'], axis=1)
    y = df['TARGET']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_STATE)

    smote = SMOTE(random_state=RANDOM_STATE)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

    return X_train_balanced, y_train_balanced, X_test, y_test

def train_and_save_model(model, params, X_train, y_train, model_name):
    grid_search = GridSearchCV(model, params, cv=5, scoring='f1')
    grid_search.fit(X_train, y_train)

    os.makedirs('models', exist_ok=True)
    model_path = f'models/{model_name}'
    if isinstance(model, xgb.XGBClassifier):
        grid_search.best_estimator_.save_model(f'{model_path}.bin')
    else:
        joblib.dump(grid_search.best_estimator_, f'{model_path}.pkl')

    print(f"Model {model_name} trained and saved.")

if __name__ == '__main__':
    X_train_balanced, y_train_balanced, X_test, y_test = (
        load_and_preprocess_data())

    # Logistic Regression
    log_reg_params = {
        'C': [0.001, 0.01, 0.1, 1, 10, 100],
        'solver': ['liblinear', 'saga']
    }
    train_and_save_model(
        LogisticRegression(max_iter=1000),
        log_reg_params,
        X_train_balanced,
        y_train_balanced,
        'logistic_regression_model'
    )

    # Random Forest
    rf_params = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, 30],
        'min_samples_split': [5, 7, 10]
    }
    train_and_save_model(
        RandomForestClassifier(),
        rf_params,
        X_train_balanced,
        y_train_balanced,
        'random_forest_model'
    )

    # XGBoost
    xgb_params = {
        'n_estimators': [75, 100, 150],
        'learning_rate': [0.2, 0.3, 0.4],
        'max_depth': [4, 5, 6]
    }
    train_and_save_model(
        xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
        xgb_params,
        X_train_balanced,
        y_train_balanced,
        'xgboost_model'
    )
