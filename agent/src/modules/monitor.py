"""
Enhanced system monitoring module for PhantomGuard Agent
"""

import os
import time
import psutil
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Callable
from collections import deque
import threading
import json

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from ..utils.logger import get_logger

logger = get_logger(__name__)

class HoneyfileHandler(FileSystemEventHandler):
    """Handler for honeyfile access detection"""

    def __init__(self, honeyfiles: Dict[str, Dict], alert_callback: Callable):
        self.honeyfiles = honeyfiles
        self.alert_callback = alert_callback
        self.access_log = deque(maxlen=100)

    def on_modified(self, event):
        """Handle file modification events"""
        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            if file_path in self.honeyfiles:
                self._handle_honeyfile_access(file_path, 'modified')

    def on_created(self, event):
        """Handle file creation events"""
        if not event.is_directory:
            file_path = os.path.abspath(event.src_path)
            if file_path in self.honeyfiles:
                self._handle_honeyfile_access(file_path, 'created')

    def on_deleted(self, event):
        """Handle file deletion events"""
        file_path = os.path.abspath(event.src_path)
        if file_path in self.honeyfiles:
            self._handle_honeyfile_access(file_path, 'deleted')

    def _handle_honeyfile_access(self, file_path: str, action: str):
        """Handle honeyfile access detection"""
        timestamp = time.time()
        honeyfile_info = self.honeyfiles[file_path]

        alert_data = {
            'type': 'honeyfile_alert',
            'file_path': file_path,
            'action': action,
            'timestamp': timestamp,
            'severity': 'critical',
            'description': f'Honeyfile {action}: {os.path.basename(file_path)}'
        }

        self.access_log.append(alert_data)
        self.alert_callback(alert_data)

        logger.critical(f"HONEYFILE ALERT: {action} - {file_path}")

class FileMonitorHandler(FileSystemEventHandler):
    """Enhanced file system event handler"""

    def __init__(self, monitor):
        self.monitor = monitor

    def on_created(self, event):
        if not event.is_directory:
            self.monitor._handle_file_event("created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.monitor._handle_file_event("modified", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.monitor._handle_file_event("deleted", event.src_path)

class EnhancedSystemMonitor:
    """Enhanced system monitoring with honeyfile detection and advanced analytics"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.running = False

        # Monitoring data buffers
        self.cpu_history = deque(maxlen=300)  # 5 minutes at 1s intervals
        self.memory_history = deque(maxlen=300)
        self.network_history = deque(maxlen=300)
        self.file_events = deque(maxlen=1000)

        # Process tracking
        self.process_cache = {}
        self.suspicious_processes = set()

        # File system monitoring
        self.observer = None
        self.file_handler = None
        self.honeyfile_handler = None

        # Honeyfile configuration
        self.honeyfiles = self._setup_honeyfiles()
        self.honeyfile_alerts = deque(maxlen=100)

        # Performance monitoring
        self.collection_times = deque(maxlen=100)

        # Threading
        self.monitor_thread = None
        self.alert_callback = None

        # Configuration
        self.monitor_paths = [
            str(Path.home() / "Downloads"),
            str(Path.home() / "Documents"),
            str(Path.home() / "Desktop"),
            str(Path.home() / "Pictures"),
            str(Path.home() / "Videos")
        ]

        # Add system paths if accessible
        if os.name == 'nt':  # Windows
            self.monitor_paths.extend([
                "C:\\Users\\Public",
                "C:\\Windows\\Temp"
            ])
        else:  # Unix-like
            self.monitor_paths.extend([
                "/tmp",
                str(Path.home() / ".config")
            ])

    def set_alert_callback(self, callback: Callable):
        """Set callback for real-time alerts"""
        self.alert_callback = callback

    def _setup_honeyfiles(self) -> Dict[str, Dict]:
        """Setup honeyfile monitoring"""
        honeyfiles = {}

        # Default honeyfile locations
        default_honeyfiles = [
            str(Path.home() / "Documents" / "important_document.docx"),
            str(Path.home() / "Desktop" / "system_config.bak"),
            str(Path.home() / "Downloads" / "critical_data.xlsx"),
        ]

        # Add system-specific honeyfiles
        if os.name == 'nt':
            default_honeyfiles.append(str(Path.home() / "AppData" / "Local" / "Temp" / "phantomguard_hosts.bak"))
        else:
            default_honeyfiles.append("/etc/hosts.bak")

        for honeyfile_path in default_honeyfiles:
            if not os.path.exists(honeyfile_path):
                try:
                    # Create the honeyfile with minimal content
                    os.makedirs(os.path.dirname(honeyfile_path), exist_ok=True)
                    with open(honeyfile_path, 'w') as f:
                        f.write("# PhantomGuard Honeyfile - DO NOT MODIFY\n")
                        f.write(f"Created: {time.time()}\n")

                    honeyfiles[honeyfile_path] = {
                        'type': 'honeyfile',
                        'created': time.time(),
                        'size': 0,
                        'hash': self._calculate_file_hash(honeyfile_path)
                    }

                    logger.info(f"Created honeyfile: {honeyfile_path}")

                except Exception as e:
                    logger.warning(f"Could not create honeyfile {honeyfile_path}: {e}")
            else:
                # File already exists, monitor it
                honeyfiles[honeyfile_path] = {
                    'type': 'existing_monitored',
                    'created': time.time(),
                    'size': os.path.getsize(honeyfile_path),
                    'hash': self._calculate_file_hash(honeyfile_path)
                }

        return honeyfiles

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except:
            return ""

    def start(self):
        """Start the enhanced monitoring system"""
        logger.info("Starting Enhanced System Monitor")

        self.running = True

        # Start file system monitoring
        self._start_file_monitoring()

        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()

        logger.info("Enhanced System Monitor started")

    def stop(self):
        """Stop the monitoring system"""
        logger.info("Stopping Enhanced System Monitor")

        self.running = False

        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=5)

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

        logger.info("Enhanced System Monitor stopped")

    def _start_file_monitoring(self):
        """Start file system monitoring"""
        try:
            # Setup file handler for general file monitoring
            self.file_handler = FileMonitorHandler(self)

            # Setup honeyfile handler
            self.honeyfile_handler = HoneyfileHandler(self.honeyfiles, self._handle_honeyfile_alert)

            # Create observer and schedule monitoring
            self.observer = Observer()

            # Monitor configured paths
            scheduled_paths = 0
            for path in self.monitor_paths:
                if os.path.exists(path):
                    try:
                        # Add general file monitoring
                        self.observer.schedule(self.file_handler, path, recursive=True)
                        scheduled_paths += 1

                        # Add honeyfile monitoring if honeyfile is in this path
                        for honeyfile in self.honeyfiles:
                            if honeyfile.startswith(path):
                                self.observer.schedule(self.honeyfile_handler, os.path.dirname(honeyfile), recursive=False)
                                break
                    except Exception as e:
                        logger.warning(f"Skipping monitor path {path}: {e}")

            if scheduled_paths == 0:
                logger.warning("No monitor paths could be scheduled")
                return

            self.observer.start()
            logger.info(f"File monitoring started for {scheduled_paths} paths")

        except Exception as e:
            logger.error(f"Failed to start file monitoring: {e}")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        logger.info("Entering monitoring loop")

        while self.running:
            try:
                start_time = time.time()

                # Collect system data
                data = self._collect_system_data()

                # Update history buffers
                self._update_history(data)

                # Performance monitoring
                collection_time = time.time() - start_time
                self.collection_times.append(collection_time)

                # Sleep for monitoring interval (adjust based on performance)
                sleep_time = max(0.1, 1.0 - collection_time)  # Target 1s intervals
                time.sleep(sleep_time)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(1)

    def collect_data(self) -> Optional[Dict[str, Any]]:
        """Collect comprehensive system data"""
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=0.1)

            # Get memory usage
            memory = psutil.virtual_memory()

            # Get disk usage
            disk_usage = self._get_disk_usage()

            # Get network stats
            network_stats = self._get_network_stats()

            # Get process information
            processes = self._get_process_info()

            # Get recent file events
            recent_events = self._get_recent_file_events()

            # Calculate metrics
            file_change_rate = len(recent_events)
            entropy = self._calculate_entropy(recent_events)

            data = {
                'timestamp': time.time(),
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'disk_usage': disk_usage,
                'network_stats': network_stats,
                'file_change_rate': file_change_rate,
                'entropy': entropy,
                'processes': processes[:20],  # Top 20 processes
                'file_events': recent_events,
                'honeyfile_alerts': list(self.honeyfile_alerts),
                'performance_metrics': self._get_performance_metrics(),
                'raw_data': {
                    'memory_total': memory.total,
                    'memory_available': memory.available,
                    'process_count': len(processes)
                }
            }

            return data

        except Exception as e:
            logger.error(f"Error collecting system data: {e}")
            return None

    def _collect_system_data(self) -> Dict[str, Any]:
        """Internal method to collect system data"""
        return self.collect_data()

    def _update_history(self, data: Dict[str, Any]):
        """Update historical data buffers"""
        if data:
            self.cpu_history.append(data['cpu_usage'])
            self.memory_history.append(data['memory_usage'])
            self.network_history.append(data['network_stats']['bytes_sent'] + data['network_stats']['bytes_recv'])

    def _get_disk_usage(self) -> Dict[str, float]:
        """Get disk usage statistics"""
        try:
            disk = psutil.disk_usage('/')
            return {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }
        except:
            return {'total': 0, 'used': 0, 'free': 0, 'percent': 0}

    def _get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        try:
            net = psutil.net_io_counters()
            return {
                'bytes_sent': net.bytes_sent,
                'bytes_recv': net.bytes_recv,
                'packets_sent': net.packets_sent,
                'packets_recv': net.packets_recv,
                'errin': net.errin,
                'errout': net.errout
            }
        except:
            return {'bytes_sent': 0, 'bytes_recv': 0, 'packets_sent': 0, 'packets_recv': 0, 'errin': 0, 'errout': 0}

    def _get_process_info(self) -> List[Dict[str, Any]]:
        """Get detailed process information"""
        processes = []

        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    proc_info = proc.info.copy()

                    # Add additional process details
                    p = psutil.Process(proc.pid)
                    proc_info.update({
                        'exe': p.exe() if p.exe() else '',
                        'cmdline': p.cmdline() if p.cmdline() else [],
                        'create_time': p.create_time(),
                        'num_threads': p.num_threads(),
                        'connections': len(p.connections()) if p.connections() else 0
                    })

                    processes.append(proc_info)

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

        except Exception as e:
            logger.error(f"Error getting process info: {e}")

        return processes

    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get monitoring performance metrics"""
        return {
            'avg_collection_time': sum(self.collection_times) / len(self.collection_times) if self.collection_times else 0,
            'cpu_history_size': len(self.cpu_history),
            'file_events_count': len(self.file_events),
            'honeyfile_count': len(self.honeyfiles)
        }

    def _handle_file_event(self, event_type: str, file_path: str):
        """Handle file system events"""
        event = {
            'timestamp': time.time(),
            'type': event_type,
            'path': file_path,
            'size': os.path.getsize(file_path) if os.path.exists(file_path) and not os.path.isdir(file_path) else 0,
            'extension': os.path.splitext(file_path)[1].lower(),
            'process_name': self._get_process_for_file(file_path)
        }

        self.file_events.append(event)

        # Keep buffer size manageable
        if len(self.file_events) > 1000:
            self.file_events.popleft()

        logger.debug(f"File event: {event_type} - {file_path}")

    def _get_recent_file_events(self, seconds: int = 10) -> List[Dict]:
        """Get file events from the last N seconds"""
        current_time = time.time()
        recent_events = [
            event for event in self.file_events
            if current_time - event['timestamp'] <= seconds
        ]
        return recent_events

    def _get_process_for_file(self, file_path: str) -> Optional[str]:
        """Get the process that modified a file (simplified)"""
        # This is a simplified implementation
        # In a real system, you'd use more sophisticated tracking
        try:
            # Check for browser processes
            browser_processes = ['chrome.exe', 'firefox.exe', 'edge.exe', 'safari.exe']
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() in [p.lower() for p in browser_processes]:
                    return proc.info['name']
        except:
            pass

        return None

    def _calculate_entropy(self, events: List[Dict]) -> float:
        """Calculate file entropy based on events (enhanced)"""
        if not events:
            return 0.0

        # Enhanced entropy calculation
        total_events = len(events)

        # Factor in file types and patterns
        suspicious_extensions = {'.docx', '.xlsx', '.pdf', '.jpg', '.png', '.mp4', '.zip', '.rar', '.enc'}
        suspicious_count = sum(1 for event in events if event.get('extension') in suspicious_extensions)

        # Time-based clustering (burst of activity)
        timestamps = [event['timestamp'] for event in events]
        if len(timestamps) > 1:
            time_spread = max(timestamps) - min(timestamps)
            avg_interval = time_spread / (len(timestamps) - 1) if len(timestamps) > 1 else 1
            burst_factor = min(1.0, avg_interval / 10.0)  # Lower interval = higher burst factor
        else:
            burst_factor = 1.0

        # Calculate entropy-like metric
        base_entropy = min(total_events / 10.0, 10.0)
        extension_entropy = suspicious_count / max(total_events, 1) * 5.0
        burst_entropy = (1 - burst_factor) * 5.0

        total_entropy = base_entropy + extension_entropy + burst_entropy

        return round(min(total_entropy, 20.0), 2)

    def _handle_honeyfile_alert(self, alert_data: Dict[str, Any]):
        """Handle honeyfile alerts"""
        self.honeyfile_alerts.append(alert_data)

        if self.alert_callback:
            self.alert_callback(alert_data)

        logger.critical(f"HONEYFILE COMPROMISE DETECTED: {alert_data}")

    def get_honeyfile_status(self) -> Dict[str, Any]:
        """Get honeyfile monitoring status"""
        return {
            'honeyfiles': self.honeyfiles,
            'recent_alerts': list(self.honeyfile_alerts),
            'total_alerts': len(self.honeyfile_alerts)
        }

    def add_honeyfile(self, file_path: str) -> bool:
        """Add a new honeyfile to monitor"""
        try:
            if not os.path.exists(file_path):
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write("# PhantomGuard Honeyfile\n")
                    f.write(f"Created: {time.time()}\n")

            self.honeyfiles[file_path] = {
                'type': 'honeyfile',
                'created': time.time(),
                'size': os.path.getsize(file_path),
                'hash': self._calculate_file_hash(file_path)
            }

            logger.info(f"Added honeyfile: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to add honeyfile {file_path}: {e}")
            return False
