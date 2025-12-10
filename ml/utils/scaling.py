import joblib
from sklearn.preprocessing import StandardScaler

def fit_scaler(X):
    sc = StandardScaler()
    sc.fit(X)
    return sc

def transform(scaler, X):
    return scaler.transform(X)

def save_scaler(scaler, path):
    joblib.dump(scaler, path)

def load_scaler(path):
    return joblib.load(path)
