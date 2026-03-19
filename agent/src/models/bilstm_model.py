"""
BiLSTM Model for Ransomware Detection
"""

import torch
import torch.nn as nn
import numpy as np
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class BiLSTMModel(nn.Module):
    """Bidirectional LSTM for sequence anomaly detection"""

    def __init__(self,
                 input_size: int = 6,
                 hidden_size: int = 64,
                 num_layers: int = 2,
                 dropout: float = 0.2):
        super(BiLSTMModel, self).__init__()

        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # BiLSTM layers
        self.bilstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0
        )

        # Attention mechanism
        self.attention = nn.Linear(hidden_size * 2, 1)

        # Fully connected layers
        self.fc1 = nn.Linear(hidden_size * 2, hidden_size)
        self.fc2 = nn.Linear(hidden_size, 1)

        # Activation functions
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the model"""
        # x shape: (batch_size, seq_len, input_size)

        # BiLSTM forward pass
        lstm_out, (h_n, c_n) = self.bilstm(x)

        # Attention mechanism
        attention_weights = torch.softmax(
            self.attention(lstm_out).squeeze(-1), dim=1
        ).unsqueeze(-1)

        # Apply attention
        attended = torch.sum(attention_weights * lstm_out, dim=1)

        # Fully connected layers
        out = self.fc1(attended)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        out = self.sigmoid(out)

        return out.squeeze(-1)

class BiLSTMDetector:
    """BiLSTM-based anomaly detector"""

    def __init__(self,
                 model_path: Optional[str] = None,
                 sequence_length: int = 50,
                 input_size: int = 6):
        self.model = None
        self.model_path = model_path
        self.sequence_length = sequence_length
        self.input_size = input_size
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Feature buffer for sequence building
        self.feature_buffer = []

        # Load model if path provided
        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path: str) -> bool:
        """Load trained BiLSTM model"""
        try:
            self.model = BiLSTMModel()
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"BiLSTM model loaded from {model_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load BiLSTM model: {e}")
            return False

    def save_model(self, model_path: str):
        """Save trained model"""
        if self.model:
            torch.save(self.model.state_dict(), model_path)
            logger.info(f"Model saved to {model_path}")

    def preprocess_features(self, features: List[float]) -> np.ndarray:
        """Preprocess features for model input"""
        # Normalize features
        features = np.array(features, dtype=np.float32)

        # Simple normalization (can be improved with proper scaling)
        features = np.clip(features, 0, 100)  # Basic clipping
        features = features / 100.0  # Scale to [0, 1]

        return features

    def build_sequence(self, features: List[float]) -> Optional[np.ndarray]:
        """Build sequence from feature buffer"""
        # Add current features to buffer
        processed_features = self.preprocess_features(features)
        self.feature_buffer.append(processed_features)

        # Keep only recent features
        if len(self.feature_buffer) > self.sequence_length:
            self.feature_buffer = self.feature_buffer[-self.sequence_length:]

        # Return sequence if we have enough data
        if len(self.feature_buffer) >= self.sequence_length:
            sequence = np.array(self.feature_buffer[-self.sequence_length:])
            return sequence

        return None

    def predict(self, sequence: np.ndarray) -> float:
        """Make prediction on sequence"""
        if self.model is None:
            return 0.5  # Neutral prediction if no model

        try:
            # Convert to tensor
            sequence_tensor = torch.FloatTensor(sequence).unsqueeze(0).to(self.device)

            # Make prediction
            with torch.no_grad():
                prediction = self.model(sequence_tensor)

            # Convert to float
            if isinstance(prediction, torch.Tensor):
                prediction = prediction.item()

            return prediction

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return 0.5

    def detect_anomaly(self, features: List[float], threshold: float = 0.8) -> Tuple[bool, float]:
        """Detect anomaly in features"""
        # Build sequence
        sequence = self.build_sequence(features)

        if sequence is None:
            return False, 0.0  # Not enough data for sequence

        # Make prediction
        prediction = self.predict(sequence)

        # Determine if anomaly
        is_anomaly = prediction > threshold

        return is_anomaly, prediction

    def reset_buffer(self):
        """Reset feature buffer"""
        self.feature_buffer = []

class ModelTrainer:
    """Trainer for BiLSTM model"""

    def __init__(self,
                 model: BiLSTMModel,
                 learning_rate: float = 0.001,
                 batch_size: int = 32):
        self.model = model
        self.learning_rate = learning_rate
        self.batch_size = batch_size

        self.criterion = nn.BCELoss()
        self.optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    def train_epoch(self, train_loader: torch.utils.data.DataLoader) -> float:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0

        for sequences, labels in train_loader:
            sequences = sequences.to(self.model.device)
            labels = labels.to(self.model.device)

            # Forward pass
            outputs = self.model(sequences)
            loss = self.criterion(outputs, labels.float())

            # Backward pass
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()

        return total_loss / len(train_loader)

    def validate(self, val_loader: torch.utils.data.DataLoader) -> Tuple[float, float]:
        """Validate model"""
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0

        with torch.no_grad():
            for sequences, labels in val_loader:
                sequences = sequences.to(self.model.device)
                labels = labels.to(self.model.device)

                outputs = self.model(sequences)
                loss = self.criterion(outputs, labels.float())

                # Calculate accuracy
                predictions = (outputs > 0.5).float()
                correct += (predictions == labels).sum().item()
                total += labels.size(0)
                total_loss += loss.item()

        accuracy = correct / total
        avg_loss = total_loss / len(val_loader)

        return avg_loss, accuracy