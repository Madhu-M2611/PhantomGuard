"""
Data sender module for PhantomGuard Agent
"""

import json
import time
import requests
from typing import Dict, Any, Optional
from queue import Queue
import threading

from ..utils.logger import get_logger

logger = get_logger(__name__)

class DataSender:
    """Send detection data to backend API"""

    def __init__(self):
        self.backend_url = "http://localhost:8000"  # Default backend URL
        self.api_key = None  # API key for authentication
        self.send_queue = Queue()
        self.running = False
        self.sender_thread = None

        # Configuration
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.batch_size = 10
        self.send_interval = 30  # seconds

    def start(self):
        """Start the data sender"""
        logger.info("Starting data sender")

        self.running = True
        self.sender_thread = threading.Thread(target=self._sender_loop, daemon=True)
        self.sender_thread.start()

        logger.info("Data sender started")

    def stop(self):
        """Stop the data sender"""
        logger.info("Stopping data sender")

        self.running = False

        if self.sender_thread and self.sender_thread.is_alive():
            self.sender_thread.join(timeout=5)

        logger.info("Data sender stopped")

    def send_data(self, data: Dict[str, Any]) -> bool:
        """Queue data for sending to backend"""
        try:
            self.send_queue.put(data)
            logger.debug("Data queued for sending")
            return True
        except Exception as e:
            logger.error(f"Failed to queue data: {e}")
            return False

    def _sender_loop(self):
        """Main sender loop"""
        logger.info("Entering sender loop")

        batch = []
        last_send_time = time.time()

        while self.running:
            try:
                # Try to get data from queue (non-blocking)
                try:
                    data = self.send_queue.get_nowait()
                    batch.append(data)

                    # Send immediately if batch is full
                    if len(batch) >= self.batch_size:
                        self._send_batch(batch)
                        batch = []
                        last_send_time = time.time()

                except:
                    pass  # No data in queue

                # Send batch if enough time has passed
                current_time = time.time()
                if batch and (current_time - last_send_time) >= self.send_interval:
                    self._send_batch(batch)
                    batch = []
                    last_send_time = current_time

                # Sleep briefly to avoid busy waiting
                time.sleep(0.1)

            except Exception as e:
                logger.error(f"Error in sender loop: {e}")
                time.sleep(1)

        # Send any remaining data before exit
        if batch:
            self._send_batch(batch)

    def _send_batch(self, batch: list):
        """Send a batch of data to the backend"""
        if not batch:
            return

        try:
            sent = 0
            for item in batch:
                log_payload = self._build_log_payload(item)
                if self._send_log(log_payload):
                    sent += 1

                for alert_payload in self._build_alert_payloads(item):
                    self._send_alert(alert_payload)

            if sent == len(batch):
                logger.info(f"Successfully sent batch of {len(batch)} items")
            else:
                logger.error(f"Sent {sent}/{len(batch)} log items successfully")

        except Exception as e:
            logger.error(f"Error sending batch: {e}")

    def _send_log(self, payload: Dict[str, Any]) -> bool:
        """Send log data to backend API"""
        url = f"{self.backend_url}/api/v1/logs/"
        headers = {
            'Content-Type': 'application/json',
        }

        # Add API key if available
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=10
                )

                if response.status_code == 200:
                    return True
                else:
                    logger.warning(f"Backend returned status {response.status_code}: {response.text}")

            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {e}")

                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        return False

    def _build_log_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize an agent detection result into the backend log schema."""
        data = payload.get('data', {})
        anomalies = payload.get('anomalies', [])
        primary_anomaly = anomalies[0] if anomalies else {}

        return {
            'file_path': primary_anomaly.get('file_path') or data.get('file_path'),
            'process_name': primary_anomaly.get('process_name') or data.get('process_name'),
            'entropy': data.get('entropy'),
            'prediction': payload.get('confidence'),
            'cpu_usage': data.get('cpu_usage'),
            'file_change_rate': data.get('file_change_rate'),
            'detection_method': primary_anomaly.get('method'),
            'raw_data': json.dumps(payload),
        }

    def _build_alert_payloads(self, payload: Dict[str, Any]) -> list:
        """Build backend alert payloads from anomalies."""
        alerts = []
        for anomaly in payload.get('anomalies', []):
            alerts.append({
                'severity': anomaly.get('severity', payload.get('severity', 'medium')),
                'title': anomaly.get('type', 'anomaly_detected'),
                'description': anomaly.get('description'),
                'file_path': anomaly.get('file_path') or payload.get('data', {}).get('file_path'),
                'process_name': anomaly.get('process_name') or payload.get('data', {}).get('process_name'),
                'detection_method': anomaly.get('method'),
                'prediction_score': anomaly.get('prediction', payload.get('confidence')),
                'raw_data': json.dumps(anomaly),
            })
        return alerts

    def _send_alert(self, alert_data: Dict[str, Any]) -> bool:
        """Send alert data to backend"""
        url = f"{self.backend_url}/api/v1/alerts/"
        headers = {
            'Content-Type': 'application/json',
        }

        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'

        try:
            response = requests.post(
                url,
                json=alert_data,
                headers=headers,
                timeout=10
            )

            if response.status_code in [200, 201]:
                logger.info("Alert sent successfully")
                return True
            else:
                logger.error(f"Failed to send alert: {response.status_code} - {response.text}")

        except requests.RequestException as e:
            logger.error(f"Failed to send alert: {e}")

        return False

    def update_config(self, backend_url: str = None, api_key: str = None):
        """Update sender configuration"""
        if backend_url:
            self.backend_url = backend_url.rstrip('/')
            logger.info(f"Backend URL updated to: {self.backend_url}")

        if api_key:
            self.api_key = api_key
            logger.info("API key updated")
