"""
Anomaly detection module for PhantomGuard Agent
"""

import time
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

from ..utils.logger import get_logger
from ..utils.feature_extractor import FeatureExtractor

try:
    from ..models.bilstm_model import BiLSTMDetector
except Exception as exc:
    BiLSTMDetector = None
    MODEL_IMPORT_ERROR = exc
else:
    MODEL_IMPORT_ERROR = None

logger = get_logger(__name__)

class AnomalyDetector:
    """Hybrid AI + rule-based anomaly detection"""

    def __init__(self):
        self.baseline_cpu = 0.0
        self.baseline_memory = 0.0
        self.baseline_file_rate = 0.0
        self.learning_period = 300  # 5 minutes learning period
        self.start_time = time.time()
        self.sample_count = 0

        # Detection thresholds
        self.z_score_threshold = 3.0
        self.entropy_threshold = 7.5
        self.file_rate_threshold = 10  # files per minute

        # BiLSTM detector
        model_path = Path(__file__).parent.parent / "models" / "bilstm_model.pth"
        self.bilstm_detector = None
        if BiLSTMDetector is not None:
            self.bilstm_detector = BiLSTMDetector(model_path=str(model_path))
        elif MODEL_IMPORT_ERROR is not None:
            logger.warning(f"BiLSTM detector unavailable, using rule-based detection only: {MODEL_IMPORT_ERROR}")

        # Feature extractor
        self.feature_extractor = FeatureExtractor()

    def detect_anomalies(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Detect anomalies in system data"""
        try:
            # Update baselines during learning period
            if time.time() - self.start_time < self.learning_period:
                self._update_baselines(data)
                return None

            anomalies = []

            # Rule-based detection
            rule_anomalies = self._rule_based_detection(data)
            anomalies.extend(rule_anomalies)

            # AI-based detection (placeholder)
            ai_anomalies = self._ai_based_detection(data)
            anomalies.extend(ai_anomalies)

            # Honeyfile detection (placeholder)
            honeyfile_anomalies = self._honeyfile_detection(data)
            anomalies.extend(honeyfile_anomalies)

            if anomalies:
                result = {
                    'timestamp': data['timestamp'],
                    'anomalies': anomalies,
                    'severity': self._calculate_severity(anomalies),
                    'confidence': self._calculate_confidence(anomalies),
                    'data': data
                }

                logger.warning(f"Anomalies detected: {len(anomalies)} events")
                return result

            return None

        except Exception as e:
            logger.error(f"Error in anomaly detection: {e}")
            return None

    def _rule_based_detection(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Rule-based anomaly detection"""
        anomalies = []

        # Z-score based detection
        cpu_z = self._calculate_z_score(data['cpu_usage'], self.baseline_cpu, 10.0)
        if abs(cpu_z) > self.z_score_threshold:
            anomalies.append({
                'type': 'cpu_anomaly',
                'method': 'rule',
                'severity': 'medium',
                'description': f'CPU usage anomaly detected (Z-score: {cpu_z:.2f})',
                'value': data['cpu_usage'],
                'threshold': self.z_score_threshold
            })

        # Entropy-based detection
        if data['entropy'] > self.entropy_threshold:
            anomalies.append({
                'type': 'entropy_anomaly',
                'method': 'rule',
                'severity': 'high',
                'description': f'High file entropy detected ({data["entropy"]:.2f})',
                'value': data['entropy'],
                'threshold': self.entropy_threshold
            })

        # File change rate detection
        if data['file_change_rate'] > self.file_rate_threshold:
            anomalies.append({
                'type': 'file_rate_anomaly',
                'method': 'rule',
                'severity': 'high',
                'description': f'High file modification rate ({data["file_change_rate"]} files/min)',
                'value': data['file_change_rate'],
                'threshold': self.file_rate_threshold
            })

        # Process-based detection
        suspicious_processes = self._detect_suspicious_processes(data.get('processes', []))
        for proc in suspicious_processes:
            anomalies.append({
                'type': 'process_anomaly',
                'method': 'rule',
                'severity': 'medium',
                'description': f'Suspicious process detected: {proc["name"]}',
                'process_name': proc['name'],
                'process_id': proc['pid']
            })

        return anomalies

    def _ai_based_detection(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """AI-based anomaly detection using BiLSTM"""
        anomalies = []

        try:
            if self.bilstm_detector is None:
                return anomalies

            # Extract features using advanced feature extractor
            features = self.feature_extractor.extract_features(data)

            # Detect anomaly using BiLSTM
            is_anomaly, prediction = self.bilstm_detector.detect_anomaly(features)

            if is_anomaly:
                anomalies.append({
                    'type': 'ai_anomaly',
                    'method': 'bilstm',
                    'severity': 'critical',
                    'description': f'BiLSTM detected ransomware pattern (confidence: {prediction:.3f})',
                    'prediction': prediction,
                    'features': features
                })

        except Exception as e:
            logger.error(f"AI detection error: {e}")

        return anomalies

    def _honeyfile_detection(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Honeyfile access detection"""
        anomalies = []

        # Check for honeyfile alerts in the data
        honeyfile_alerts = data.get('honeyfile_alerts', [])
        for alert in honeyfile_alerts:
            anomalies.append({
                'type': 'honeyfile_violation',
                'method': 'honeyfile',
                'severity': 'critical',
                'description': alert.get('description', 'Honeyfile accessed'),
                'file_path': alert.get('file_path'),
                'action': alert.get('action'),
                'timestamp': alert.get('timestamp')
            })

        return anomalies

    def _calculate_z_score(self, value: float, mean: float, std: float) -> float:
        """Calculate Z-score"""
        if std == 0:
            return 0.0
        return (value - mean) / std

    def _detect_suspicious_processes(self, processes: List[Dict]) -> List[Dict]:
        """Detect suspicious processes"""
        suspicious = []

        # Known suspicious process patterns
        suspicious_patterns = [
            'ransomware',
            'encrypt',
            'malware',
            'trojan',
            'virus'
        ]

        for proc in processes:
            proc_name = proc.get('name', '').lower()
            for pattern in suspicious_patterns:
                if pattern in proc_name:
                    suspicious.append(proc)
                    break

        return suspicious

    def _update_baselines(self, data: Dict[str, Any]):
        """Update baseline statistics during learning period"""
        self.sample_count += 1

        # Simple moving average for baselines
        alpha = 1.0 / self.sample_count

        self.baseline_cpu = (1 - alpha) * self.baseline_cpu + alpha * data['cpu_usage']
        self.baseline_memory = (1 - alpha) * self.baseline_memory + alpha * data['memory_usage']
        self.baseline_file_rate = (1 - alpha) * self.baseline_file_rate + alpha * data['file_change_rate']

    def _extract_features(self, data: Dict[str, Any]) -> List[float]:
        """Extract features for AI model (legacy method - use FeatureExtractor instead)"""
        # This method is kept for backward compatibility but delegates to FeatureExtractor
        return self.feature_extractor.extract_features(data)

    def _calculate_severity(self, anomalies: List[Dict]) -> str:
        """Calculate overall severity"""
        severity_levels = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}

        max_severity = max(
            (severity_levels.get(anomaly.get('severity', 'low'), 1) for anomaly in anomalies),
            default=1
        )

        severity_map = {1: 'low', 2: 'medium', 3: 'high', 4: 'critical'}
        return severity_map[max_severity]

    def _calculate_confidence(self, anomalies: List[Dict]) -> float:
        """Calculate overall confidence score"""
        if not anomalies:
            return 0.0

        # Simple confidence calculation
        ai_confidence = sum(
            anomaly.get('prediction', 0.5)
            for anomaly in anomalies
            if anomaly.get('method') == 'bilstm'
        )

        rule_confidence = len([
            a for a in anomalies
            if a.get('method') == 'rule'
        ]) * 0.7

        total_confidence = (ai_confidence + rule_confidence) / len(anomalies)
        return min(total_confidence, 1.0)
