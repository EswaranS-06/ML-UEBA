ISOLATION_FOREST_PARAMS = {
    "n_estimators": 200,
    "max_samples": "auto",
    "contamination": 0.01,
    "random_state": 42
}

LSTM_AUTOENCODER_PARAMS = {
    "latent_dim": 32,
    "hidden_dim": 64,
    "num_layers": 1,
    "dropout": 0.1,
    "lr": 1e-3,
    "batch_size": 64,
    "epochs": 10
}

MODEL_DIR = "models/"
