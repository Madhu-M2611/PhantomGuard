"""
BiLSTM Model Training Script for Ransomware Detection
"""

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
from pathlib import Path
import argparse
import logging
from typing import List, Tuple
import json

from models.bilstm_model import BiLSTMModel, ModelTrainer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SequenceDataset(Dataset):
    """Dataset for sequence data"""

    def __init__(self, sequences: np.ndarray, labels: np.ndarray):
        self.sequences = torch.FloatTensor(sequences)
        self.labels = torch.FloatTensor(labels)

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return self.sequences[idx], self.labels[idx]

def generate_synthetic_data(num_samples: int = 10000,
                          sequence_length: int = 50,
                          input_size: int = 6) -> Tuple[np.ndarray, np.ndarray]:
    """Generate synthetic training data"""

    sequences = []
    labels = []

    for _ in range(num_samples):
        # Generate normal behavior sequences
        if np.random.random() > 0.3:  # 70% normal
            sequence = generate_normal_sequence(sequence_length, input_size)
            label = 0
        else:  # 30% anomalous
            sequence = generate_anomalous_sequence(sequence_length, input_size)
            label = 1

        sequences.append(sequence)
        labels.append(label)

    return np.array(sequences), np.array(labels)

def generate_normal_sequence(length: int, input_size: int) -> np.ndarray:
    """Generate normal behavior sequence"""
    sequence = []

    for _ in range(length):
        # Normal ranges for features
        cpu = np.random.normal(20, 5)  # CPU usage 15-25%
        memory = np.random.normal(50, 10)  # Memory usage 40-60%
        file_rate = np.random.normal(2, 1)  # File changes 1-3 per minute
        entropy = np.random.normal(4, 1)  # Entropy 3-5
        processes = np.random.poisson(50)  # ~50 processes
        file_events = np.random.poisson(5)  # ~5 file events

        # Clip to reasonable ranges
        features = [
            np.clip(cpu, 0, 100),
            np.clip(memory, 0, 100),
            np.clip(file_rate, 0, 20),
            np.clip(entropy, 0, 10),
            np.clip(processes, 0, 200),
            np.clip(file_events, 0, 50)
        ]

        sequence.append(features)

    return np.array(sequence)

def generate_anomalous_sequence(length: int, input_size: int) -> np.ndarray:
    """Generate anomalous (ransomware-like) behavior sequence"""
    sequence = []

    # Start with normal behavior
    for i in range(length // 2):
        sequence.append(generate_normal_sequence(1, input_size)[0])

    # Transition to anomalous behavior
    for i in range(length // 2):
        # Ransomware characteristics:
        # - High CPU usage
        # - High file change rate
        # - High entropy (encrypted files)
        # - Increasing over time

        progress = i / (length // 2)  # 0 to 1

        cpu = 80 + np.random.normal(10 * progress, 5)  # CPU spikes
        memory = 70 + np.random.normal(15 * progress, 5)  # Memory increases
        file_rate = 50 + np.random.normal(20 * progress, 5)  # Massive file changes
        entropy = 8 + np.random.normal(1 * progress, 0.5)  # High entropy
        processes = np.random.poisson(30)  # Fewer processes (system strain)
        file_events = 100 + np.random.poisson(50 * progress)  # Lots of file events

        features = [
            np.clip(cpu, 0, 100),
            np.clip(memory, 0, 100),
            np.clip(file_rate, 0, 200),
            np.clip(entropy, 0, 10),
            np.clip(processes, 0, 200),
            np.clip(file_events, 0, 500)
        ]

        sequence.append(features)

    return np.array(sequence)

def create_data_loaders(sequences: np.ndarray,
                       labels: np.ndarray,
                       batch_size: int = 32,
                       train_split: float = 0.8) -> Tuple[DataLoader, DataLoader]:
    """Create train and validation data loaders"""

    # Shuffle data
    indices = np.random.permutation(len(sequences))
    sequences = sequences[indices]
    labels = labels[indices]

    # Split
    split_idx = int(len(sequences) * train_split)
    train_sequences = sequences[:split_idx]
    train_labels = labels[:split_idx]
    val_sequences = sequences[split_idx:]
    val_labels = labels[split_idx:]

    # Create datasets
    train_dataset = SequenceDataset(train_sequences, train_labels)
    val_dataset = SequenceDataset(val_sequences, val_labels)

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader

def train_model(num_epochs: int = 50,
               batch_size: int = 32,
               learning_rate: float = 0.001,
               save_path: str = "models/bilstm_model.pth"):
    """Train the BiLSTM model"""

    logger.info("Generating synthetic training data...")
    sequences, labels = generate_synthetic_data(num_samples=5000)

    logger.info(f"Generated {len(sequences)} sequences")
    logger.info(f"Normal samples: {np.sum(labels == 0)}")
    logger.info(f"Anomalous samples: {np.sum(labels == 1)}")

    # Create data loaders
    train_loader, val_loader = create_data_loaders(sequences, labels, batch_size)

    # Initialize model
    model = BiLSTMModel()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # Initialize trainer
    trainer = ModelTrainer(model, learning_rate, batch_size)

    # Training loop
    best_accuracy = 0.0
    patience = 10
    patience_counter = 0

    logger.info("Starting training...")

    for epoch in range(num_epochs):
        # Train
        train_loss = trainer.train_epoch(train_loader)

        # Validate
        val_loss, val_accuracy = trainer.validate(val_loader)

        logger.info(f"Epoch {epoch+1}/{num_epochs}")
        logger.info(".4f")
        logger.info(".4f")

        # Save best model
        if val_accuracy > best_accuracy:
            best_accuracy = val_accuracy
            patience_counter = 0

            # Create models directory if it doesn't exist
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            torch.save(model.state_dict(), save_path)
            logger.info(f"Model saved to {save_path}")
        else:
            patience_counter += 1

        # Early stopping
        if patience_counter >= patience:
            logger.info("Early stopping triggered")
            break

    logger.info("Training completed!")
    logger.info(".4f")

def evaluate_model(model_path: str, test_sequences: np.ndarray = None, test_labels: np.ndarray = None):
    """Evaluate trained model"""

    if test_sequences is None or test_labels is None:
        # Generate test data
        test_sequences, test_labels = generate_synthetic_data(num_samples=1000)

    # Load model
    model = BiLSTMModel()
    model.load_state_dict(torch.load(model_path))
    model.eval()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)

    # Create test dataset
    test_dataset = SequenceDataset(test_sequences, test_labels)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # Evaluate
    trainer = ModelTrainer(model)
    test_loss, test_accuracy = trainer.validate(test_loader)

    logger.info("Model Evaluation:")
    logger.info(".4f")
    logger.info(".4f")

    return test_loss, test_accuracy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train BiLSTM model for ransomware detection")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--save_path", type=str, default="models/bilstm_model.pth", help="Model save path")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate existing model")

    args = parser.parse_args()

    if args.evaluate:
        evaluate_model(args.save_path)
    else:
        train_model(args.epochs, args.batch_size, args.lr, args.save_path)