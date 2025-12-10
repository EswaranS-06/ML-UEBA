import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import joblib

from ml.models.base import BaseAnomalyModel
from ml.config import LSTM_AUTOENCODER_PARAMS


class LSTMAE(nn.Module):
    def __init__(self, input_dim, hidden_dim, latent_dim):
        super().__init__()
        self.encoder = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, latent_dim)
        self.decoder = nn.LSTM(latent_dim, hidden_dim, batch_first=True)
        self.output = nn.Linear(hidden_dim, input_dim)

    def forward(self, x):
        _, (h, _) = self.encoder(x)
        z = self.fc(h[-1]).unsqueeze(1)
        dec, _ = self.decoder(z)
        return self.output(dec)


class LSTMAutoencoder(BaseAnomalyModel):

    def __init__(self):
        self.params = LSTM_AUTOENCODER_PARAMS
        self.device = torch.device("cpu")
        self.model = None
        self.threshold = None
        self.input_dim = None

    def _build_model(self):
        self.model = LSTMAE(
            input_dim=self.input_dim,
            hidden_dim=self.params["hidden_dim"],
            latent_dim=self.params["latent_dim"]
        ).to(self.device)

    def fit(self, X):
        X = X.astype("float32")
        N, D = X.shape
        self.input_dim = D
        self._build_model()

        loader = DataLoader(
            TensorDataset(torch.tensor(X).unsqueeze(1)),
            batch_size=self.params["batch_size"],
            shuffle=True
        )

        optim = torch.optim.Adam(self.model.parameters(), lr=self.params["lr"])
        loss_fn = nn.MSELoss()

        self.model.train()
        for _ in range(self.params["epochs"]):
            for (b,) in loader:
                optim.zero_grad()
                recon = self.model(b)
                loss = loss_fn(recon, b)
                loss.backward()
                optim.step()

        errors = self.score(X)
        self.threshold = np.percentile(errors, 99)

    def score(self, X):
        if self.model is None:
            raise RuntimeError("LSTM Autoencoder not loaded or trained")

        with torch.no_grad():
            x = torch.tensor(X).unsqueeze(1)
            recon = self.model(x)
            return torch.mean((recon - x) ** 2, dim=(1, 2)).numpy()

    def save(self, path):
        joblib.dump({
            "state_dict": self.model.state_dict(),
            "threshold": self.threshold,
            "input_dim": self.input_dim
        }, path)

    def load(self, path):
        data = joblib.load(path)
        self.threshold = data["threshold"]
        self.input_dim = data["input_dim"]
        self._build_model()
        self.model.load_state_dict(data["state_dict"])
        self.model.eval()
