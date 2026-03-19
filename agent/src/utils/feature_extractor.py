"""
Feature Engineering for Ransomware Detection
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from collections import deque
import time
import hashlib
import math
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class FeatureExtractor:
    """Feature extraction and preprocessing for ransomware detection"""

    def __init__(self,
                 window_size: int = 50,
                 max_processes: int = 100,
                 max_files: int = 1000):
        self.window_size = window_size
        self.max_processes = max_processes
        self.max_files = max_files

        # Rolling windows for time-series features
        self.cpu_history = deque(maxlen=window_size)
        self.memory_history = deque(maxlen=window_size)
        self.file_rate_history = deque(maxlen=window_size)
        self.entropy_history = deque(maxlen=window_size)

        # Process monitoring
        self.process_history = deque(maxlen=max_processes)
        self.file_events = deque(maxlen=max_files)

        # Statistical accumulators
        self.cpu_stats = {'mean': 0.0, 'std': 1.0, 'count': 0}
        self.memory_stats = {'mean': 0.0, 'std': 1.0, 'count': 0}
        self.file_rate_stats = {'mean': 0.0, 'std': 1.0, 'count': 0}
        self.entropy_stats = {'mean': 0.0, 'std': 1.0, 'count': 0}

    def extract_features(self, data: Dict[str, Any]) -> List[float]:
        """Extract features from system data"""

        # Basic system metrics
        cpu_usage = float(data.get('cpu_usage', 0.0))
        memory_usage = float(data.get('memory_usage', 0.0))
        file_change_rate = float(data.get('file_change_rate', 0.0))
        entropy = float(data.get('entropy', 0.0))

        # Update rolling windows
        self.cpu_history.append(cpu_usage)
        self.memory_history.append(memory_usage)
        self.file_rate_history.append(file_change_rate)
        self.entropy_history.append(entropy)

        # Update statistics
        self._update_statistics()

        # Extract features
        features = []

        # Raw metrics
        features.append(cpu_usage)
        features.append(memory_usage)
        features.append(file_change_rate)
        features.append(entropy)

        # Statistical features
        features.extend(self._extract_statistical_features())

        # Time-series features
        features.extend(self._extract_time_series_features())

        # Process features
        process_features = self._extract_process_features(data.get('processes', []))
        features.extend(process_features)

        # File system features
        file_features = self._extract_file_features(data.get('file_events', []))
        features.extend(file_features)

        # Behavioral features
        behavioral_features = self._extract_behavioral_features(data)
        features.extend(behavioral_features)

        return features

    def _update_statistics(self):
        """Update running statistics"""
        for name, history, stats in [
            ('cpu', self.cpu_history, self.cpu_stats),
            ('memory', self.memory_history, self.memory_stats),
            ('file_rate', self.file_rate_history, self.file_rate_stats),
            ('entropy', self.entropy_history, self.entropy_stats)
        ]:
            if len(history) > 1:
                values = list(history)
                stats['mean'] = np.mean(values)
                stats['std'] = np.std(values) + 1e-6  # Avoid division by zero
                stats['count'] = len(values)

    def _extract_statistical_features(self) -> List[float]:
        """Extract statistical features"""
        features = []

        # Z-scores
        if len(self.cpu_history) > 1:
            cpu_z = (self.cpu_history[-1] - self.cpu_stats['mean']) / self.cpu_stats['std']
            features.append(cpu_z)
        else:
            features.append(0.0)

        if len(self.memory_history) > 1:
            memory_z = (self.memory_history[-1] - self.memory_stats['mean']) / self.memory_stats['std']
            features.append(memory_z)
        else:
            features.append(0.0)

        if len(self.file_rate_history) > 1:
            file_rate_z = (self.file_rate_history[-1] - self.file_rate_stats['mean']) / self.file_rate_stats['std']
            features.append(file_rate_z)
        else:
            features.append(0.0)

        if len(self.entropy_history) > 1:
            entropy_z = (self.entropy_history[-1] - self.entropy_stats['mean']) / self.entropy_stats['std']
            features.append(entropy_z)
        else:
            features.append(0.0)

        # Rate of change
        if len(self.cpu_history) > 1:
            cpu_roc = self.cpu_history[-1] - self.cpu_history[-2]
            features.append(cpu_roc)
        else:
            features.append(0.0)

        if len(self.file_rate_history) > 1:
            file_rate_roc = self.file_rate_history[-1] - self.file_rate_history[-2]
            features.append(file_rate_roc)
        else:
            features.append(0.0)

        return features

    def _extract_time_series_features(self) -> List[float]:
        """Extract time-series features"""
        features = []

        # Trend analysis
        if len(self.cpu_history) >= 5:
            cpu_trend = np.polyfit(range(len(self.cpu_history)), list(self.cpu_history), 1)[0]
            features.append(cpu_trend)
        else:
            features.append(0.0)

        if len(self.file_rate_history) >= 5:
            file_trend = np.polyfit(range(len(self.file_rate_history)), list(self.file_rate_history), 1)[0]
            features.append(file_trend)
        else:
            features.append(0.0)

        # Volatility
        if len(self.cpu_history) > 1:
            cpu_volatility = np.std(list(self.cpu_history))
            features.append(cpu_volatility)
        else:
            features.append(0.0)

        if len(self.file_rate_history) > 1:
            file_volatility = np.std(list(self.file_rate_history))
            features.append(file_volatility)
        else:
            features.append(0.0)

        return features

    def _extract_process_features(self, processes: List[Dict]) -> List[float]:
        """Extract process-related features"""
        features = []

        if not processes:
            return [0.0] * 5

        # Process counts
        total_processes = len(processes)
        features.append(total_processes)

        # Suspicious process indicators
        suspicious_count = 0
        high_cpu_processes = 0
        new_processes = 0

        current_time = time.time()

        for proc in processes:
            # Check for suspicious names
            name = proc.get('name', '').lower()
            if any(keyword in name for keyword in ['encrypt', 'ransom', 'malware', 'trojan']):
                suspicious_count += 1

            # High CPU usage
            if proc.get('cpu_percent', 0) > 50:
                high_cpu_processes += 1

            # Recently created processes
            if current_time - proc.get('create_time', current_time) < 60:  # Last minute
                new_processes += 1

        features.append(suspicious_count)
        features.append(high_cpu_processes)
        features.append(new_processes)

        # Process entropy (diversity)
        if processes:
            names = [p.get('name', '') for p in processes]
            name_entropy = self._calculate_entropy(names)
            features.append(name_entropy)
        else:
            features.append(0.0)

        return features

    def _extract_file_features(self, file_events: List[Dict]) -> List[float]:
        """Extract file system features"""
        features = []

        if not file_events:
            return [0.0] * 6

        # File operation counts
        created = sum(1 for e in file_events if e.get('event_type', e.get('type')) == 'created')
        modified = sum(1 for e in file_events if e.get('event_type', e.get('type')) == 'modified')
        deleted = sum(1 for e in file_events if e.get('event_type', e.get('type')) == 'deleted')

        features.extend([created, modified, deleted])

        # File type analysis
        extensions = []
        for event in file_events:
            path = event.get('path', '')
            if '.' in path:
                ext = path.split('.')[-1].lower()
                extensions.append(ext)

        # Common ransomware target extensions
        suspicious_exts = ['doc', 'docx', 'xls', 'xlsx', 'pdf', 'jpg', 'png', 'txt']
        suspicious_count = sum(1 for ext in extensions if ext in suspicious_exts)

        features.append(suspicious_count)

        # File entropy (if available)
        if file_events and 'entropy' in file_events[0]:
            avg_entropy = np.mean([e.get('entropy', 0) for e in file_events])
            features.append(avg_entropy)
        else:
            features.append(0.0)

        return features

    def _extract_behavioral_features(self, data: Dict[str, Any]) -> List[float]:
        """Extract behavioral pattern features"""
        features = []

        # Network activity (placeholder)
        network_connections = data.get('network_connections', 0)
        features.append(network_connections)

        # Disk I/O
        disk_read = data.get('disk_read_bytes', 0)
        disk_write = data.get('disk_write_bytes', 0)
        features.extend([disk_read, disk_write])

        # System calls (placeholder)
        system_calls = data.get('system_calls', 0)
        features.append(system_calls)

        return features

    def _calculate_entropy(self, items: List[str]) -> float:
        """Calculate Shannon entropy of a list of items"""
        if not items:
            return 0.0

        # Count frequencies
        freq = {}
        for item in items:
            freq[item] = freq.get(item, 0) + 1

        # Calculate entropy
        entropy = 0.0
        total = len(items)

        for count in freq.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)

        return entropy

    def calculate_file_entropy(self, file_path: str) -> float:
        """Calculate entropy of a file"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()

            if not data:
                return 0.0

            # Calculate byte frequencies
            freq = [0] * 256
            for byte in data:
                freq[byte] += 1

            # Calculate entropy
            entropy = 0.0
            data_len = len(data)

            for count in freq:
                if count > 0:
                    p = count / data_len
                    entropy -= p * math.log2(p)

            return entropy

        except Exception as e:
            logger.error(f"Error calculating file entropy: {e}")
            return 0.0

    def reset(self):
        """Reset all internal state"""
        self.cpu_history.clear()
        self.memory_history.clear()
        self.file_rate_history.clear()
        self.entropy_history.clear()
        self.process_history.clear()
        self.file_events.clear()

        # Reset statistics
        for stats in [self.cpu_stats, self.memory_stats, self.file_rate_stats, self.entropy_stats]:
            stats['mean'] = 0.0
            stats['std'] = 1.0
            stats['count'] = 0
