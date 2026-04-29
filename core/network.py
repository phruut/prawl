import threading
import time
import psutil
import re
from socket import gethostbyaddr, herror
from ._utils import sleep

import logging
logger = logging.getLogger('prawl')

class Network:
    """monitors network connections for process, tracks connections to specific ports and hosts"""
    def __init__(self, config, process):
        self.config = config
        self.process = process

        self._running = False
        self._check_interval = 0.5
        self._monitor_thread = None
        self._lock = threading.Lock()
        self._active_connections = set()
        self._base_connections = set()

        # dns cache to avoid repeating lookups
        self._dns_cache = {}
        self._dns_cache_time = {}
        self._dns_cache_ttl = 60

        # check ports to monitor gfrom config
        port_range = self.config.network.get('network', 'match_ports')
        start_port, end_port = map(int, port_range.split('-'))
        self._target_ports = range(start_port, end_port + 1)

        # regex pattern to match hostnames
        host_pattern_str = self.config.network.get('network', 'host_patterns')
        self._host_pattern = re.compile(host_pattern_str)

    def start(self):
        """start monitoring network connections in background thread"""
        if self._running:
            return
        logger.info(f'network monitor started | ports: {list(self._target_ports)}')
        self._running = True
        self._active_connections = set()
        self._dns_cache.clear()
        self._dns_cache_time.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def stop(self):
        """stop monitoring and wait for background thread to finish"""
        logger.info('network monitor stopped')
        self._running = False
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1.0)
        self._monitor_thread = None

    def update_base(self):
        """capture current connections as baseline"""
        with self._lock:
            self._base_connections = self._active_connections.copy()
        logger.debug(f'base updated, ignoring: {self._base_connections}')

    def is_match_active(self):
        """check new connections outside baseline"""
        with self._lock:
            match_connections = self._active_connections - self._base_connections
        return len(match_connections) > 0

    def get_connections(self):
        """return currently tracked connections"""
        with self._lock:
            return self._active_connections.copy()

    def _resolve_match(self, ip, port):
        """resolve ip to hostname and cache it, returns 'hostname:port' if hostname matches, else none"""
        now = time.time()

        # check cache
        if ip in self._dns_cache:
            # expire stale entries
            if now - self._dns_cache_time[ip] > self._dns_cache_ttl:
                del self._dns_cache[ip]
                del self._dns_cache_time[ip]
            else:
                hostname = self._dns_cache[ip]
                if hostname and self._host_pattern.search(hostname):
                    return f"{hostname}:{port}"
                return None

        # cache miss, do lookup
        try:
            hostname = gethostbyaddr(ip)[0]
            self._dns_cache[ip] = hostname
            self._dns_cache_time[ip] = now
            if self._host_pattern.search(hostname):
                return f"{hostname}:{port}"
        except herror:
            # dns lookup failed, host not found
            self._dns_cache[ip] = None
            self._dns_cache_time[ip] = now
        except Exception as e:
            logger.debug(f'dns error: {e}')

        return None

    def _scan_connections(self, proc):
        """scan process for active inet connections matching target ports and hostname pattern"""
        matches = set()
        try:
            # get all connections for process
            connections = proc.net_connections(kind='inet')

            for conn in connections:
                # skips connections without remote address or not in target port range
                if not conn.raddr or conn.raddr.port not in self._target_ports:
                    continue

                # resolve ip to hostname, check if regex pattern match
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
        """compare current connections with cached state, also update cache"""
        with self._lock:
            if current_set == self._active_connections:
                return

            # calculate changes
            added = current_set - self._active_connections
            removed = self._active_connections - current_set

            if added:
                logger.info(f'+ added {added}')
            if removed:
                logger.info(f'- removed {removed}')

            self._active_connections = current_set

    def _monitor_loop(self):
        """background loop to scan for new connections"""
        cached_pid = None
        proc = None

        while self._running:
            pid = self.process.get_pid()

            # get process reference if pid changed
            if pid != cached_pid:
                proc = psutil.Process(pid) if pid else None
                cached_pid = pid

            # scan for matching connections
            current_set = self._scan_connections(proc) if proc else set()
            self._sync_state(current_set)
            sleep(self._check_interval)
