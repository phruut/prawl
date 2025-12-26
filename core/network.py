import threading
import psutil
import re
from socket import gethostbyaddr, herror
from ._utils import sleep

import logging
logger = logging.getLogger('prawl')

class Network:
    def __init__(self, config, process):
        self.config = config
        self.process = process

        self._running = False
        self._check_interval = 0.5
        self._monitor_thread = None
        self._active_connections = set()
        self._base_connections = set()

        port_range = self.config.network.get('network', 'match_ports')
        start_port, end_port = map(int, port_range.split('-'))
        self._target_ports = range(start_port, end_port + 1)

        host_pattern_str = self.config.network.get('network', 'host_patterns')
        self._host_pattern = re.compile(host_pattern_str)

    def start(self):
        if self._running:
            return
        logger.info(f'watching ports: {list(self._target_ports)}')
        self._running = True
        self._active_connections = set()
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def stop(self):
        self._running = False
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1.0)
        self._monitor_thread = None

    def update_base(self):
        self._base_connections = self._active_connections.copy()
        logger.debug(f'base updated, ignoring: {self._base_connections}')

    def is_match_active(self):
        match_connections = self._active_connections - self._base_connections
        return len(match_connections) > 0

    def get_connections(self):
        return self._active_connections.copy()

    def _resolve_match(self, ip, port):
        """ip to hostname"""
        try:
            hostname = gethostbyaddr(ip)[0]
            if self._host_pattern.search(hostname):
                return f"{hostname}:{port}"
        except herror:
            pass  # DNS lookup failed gracefully
        except Exception as e:
            logger.debug(f'dns error: {e}')

        return None

    def _scan_connections(self, pid):
        """scan process for active inet connections matching target ports"""
        matches = set()
        try:
            proc = psutil.Process(pid)
            connections = proc.net_connections(kind='inet')

            for conn in connections:
                if not conn.raddr or conn.raddr.port not in self._target_ports:
                    continue

                match_id = self._resolve_match(conn.raddr.ip, conn.raddr.port)
                if match_id:
                    matches.add(match_id)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # process died or lost permissions
            pass
        except Exception as e:
            logger.debug(f'error: {e}')

        return matches

    def _sync_state(self, current_set):
        """compare current connections with cached state, logs diffs, updates cache"""
        if current_set == self._active_connections:
            return

        added = current_set - self._active_connections
        removed = self._active_connections - current_set

        if added:
            logger.info(f'+ added {added}')
        if removed:
            logger.info(f'- removed {removed}')

        self._active_connections = current_set

    def _monitor_loop(self):
        while self._running:
            pid = self.process.get_pid()
            current_set = self._scan_connections(pid) if pid else set()
            self._sync_state(current_set)
            sleep(self._check_interval)
