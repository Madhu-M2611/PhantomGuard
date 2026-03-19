#!/usr/bin/env python3
"""
Quick test script for BiLSTM model functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import torch
    import numpy as np
    from models.bilstm_model import BiLSTMModel, BiLSTMDetector

    def test_model_creation():
        """Test model creation and basic functionality"""
        print("Testing BiLSTM model creation...")

        # Create model
        model = BiLSTMModel()
        print(f"✓ Model created with {sum(p.numel() for p in model.parameters())} parameters")

        # Test forward pass
        batch_size, seq_len, input_size = 2, 10, 6
        test_input = torch.randn(batch_size, seq_len, input_size)

        with torch.no_grad():
            output = model(test_input)
            print(f"✓ Forward pass successful, output shape: {output.shape}")

        return True

    def test_detector_creation():
        """Test detector creation"""
        print("Testing BiLSTM detector creation...")

        detector = BiLSTMDetector()
        print("✓ Detector created without model file")

        # Test feature processing
        features = [10.0, 50.0, 5.0, 4.0, 45, 8]  # Sample features
        is_anomaly, prediction = detector.detect_anomaly(features)
        print(f"✓ Detection test completed: anomaly={is_anomaly}, prediction={prediction:.3f}")

        return True

    def test_feature_extraction():
        """Test feature extraction"""
        print("Testing feature extraction...")

        from utils.feature_extractor import FeatureExtractor

        extractor = FeatureExtractor()

        # Sample data
        sample_data = {
            'cpu_usage': 25.0,
            'memory_usage': 60.0,
            'file_change_rate': 3.0,
            'entropy': 4.5,
            'processes': [{'name': 'chrome.exe', 'cpu_percent': 5.0}],
            'file_events': [{'event_type': 'modified', 'path': 'test.txt'}]
        }

        features = extractor.extract_features(sample_data)
        print(f"✓ Feature extraction successful, {len(features)} features extracted")

        return True

    if __name__ == "__main__":
        print("🚀 Starting BiLSTM Model Tests")
        print("=" * 50)

        try:
            test_model_creation()
            print()

            test_detector_creation()
            print()

            test_feature_extraction()
            print()

            print("✅ All tests passed! BiLSTM implementation is working.")

        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install torch numpy")
    sys.exit(1)