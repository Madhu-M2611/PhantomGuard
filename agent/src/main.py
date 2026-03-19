#!/usr/bin/env python3
"""
PhantomGuard 2.0 Agent - Python Monitoring System
"""

import sys
import time
import signal
import argparse

from loguru import logger

try:
    from .modules.monitor import EnhancedSystemMonitor
    from .modules.detector import AnomalyDetector
    from .modules.sender import DataSender
except ImportError:
    from modules.monitor import EnhancedSystemMonitor
    from modules.detector import AnomalyDetector
    from modules.sender import DataSender


class PhantomGuardAgent:
    """Main PhantomGuard monitoring agent"""

    def __init__(self, config_path: str = None):
        self.config_path = config_path or "config.yaml"
        self.monitor = None
        self.detector = None
        self.sender = None
        self.running = False

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop()

    def start(self):
        """Start the monitoring agent"""
        try:
            logger.info("Starting PhantomGuard Agent v2.0.42_PROT")

            self.monitor = EnhancedSystemMonitor()
            self.detector = AnomalyDetector()
            self.sender = DataSender()

            self.monitor.set_alert_callback(self._handle_realtime_alert)
            self._load_config()
            self.monitor.start()
            self.sender.start()

            self.running = True
            logger.info("Agent started successfully")
            self._run_monitoring_loop()

        except Exception as exc:
            logger.error(f"Failed to start agent: {exc}")
            self.stop()
            sys.exit(1)

    def stop(self):
        """Stop the monitoring agent"""
        self.running = False
        logger.info("Agent stopped")

        if self.monitor:
            self.monitor.stop()
        if self.sender:
            self.sender.stop()

    def _load_config(self):
        """Load agent configuration"""
        logger.info("Configuration loaded")

    def _handle_realtime_alert(self, alert_data):
        """Forward monitor alerts to the sender queue."""
        if not self.sender:
            return

        payload = {
            "timestamp": alert_data.get("timestamp", time.time()),
            "anomalies": [{
                "type": alert_data.get("type", "realtime_alert"),
                "method": "honeyfile",
                "severity": alert_data.get("severity", "critical"),
                "description": alert_data.get("description", "Realtime alert detected"),
                "file_path": alert_data.get("file_path"),
                "process_name": alert_data.get("process_name"),
                "action": alert_data.get("action"),
            }],
            "severity": alert_data.get("severity", "critical"),
            "confidence": 1.0,
            "data": {
                "file_path": alert_data.get("file_path"),
                "process_name": alert_data.get("process_name"),
                "raw_alert": alert_data,
            },
        }
        self.sender.send_data(payload)

    def _run_monitoring_loop(self):
        """Main monitoring loop"""
        logger.info("Entering monitoring loop")

        while self.running:
            try:
                system_data = self.monitor.collect_data()
                if system_data:
                    detection_result = self.detector.detect_anomalies(system_data)
                    if detection_result:
                        self.sender.send_data(detection_result)

                time.sleep(1)

            except Exception as exc:
                logger.error(f"Error in monitoring loop: {exc}")
                time.sleep(5)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="PhantomGuard 2.0 Agent")
    parser.add_argument("--config", "-c", help="Path to configuration file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    log_level = "DEBUG" if args.verbose else "INFO"
    logger.remove()
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )

    agent = PhantomGuardAgent(config_path=args.config)
    agent.start()


if __name__ == "__main__":
    main()
