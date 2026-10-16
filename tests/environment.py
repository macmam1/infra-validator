#!/usr/bin/env python3
"""Environment check — OS, CPU, RAM, disk, uptime."""
import os
import platform
import shutil
import subprocess

def get_memory_mb():
    """Get available memory in MB."""
    try:
        with open('/proc/meminfo') as f:
            for line in f:
                if line.startswith('MemAvailable:'):
                    return int(line.split()[1]) / 1024
                if line.startswith('MemTotal:'):
                    return int(line.split()[1]) / 1024
    except:
        return None

def get_disk_gb():
    """Get disk space in GB."""
    usage = shutil.disk_usage('/')
    return round(usage.total / (1024**3, 2), 2)

def get_cpu_info():
    """Get CPU info."""
    try:
        result = subprocess.run(['nproc'], capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except:
        return None

def get_uptime():
    """Get uptime in seconds."""
    try:
        with open('/proc/uptime') as f:
            return float(f.read().split()[0])
    except:
        return None

def check():
    return {
        "os": platform.platform(),
        "hostname": platform.node(),
        "cpu_count": get_cpu_info(),
        "memory_mb": get_memory_mb(),
        "disk_gb": get_disk_gb(),
        "uptime_seconds": get_uptime(),
        "arch": platform.machine(),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(check(), indent=2))
