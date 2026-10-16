#!/usr/bin/env python3
"""Background process check — can we run a daemon?"""
import subprocess
import time
import json
import os
import signal

def check():
    results = {}

    # Test 1: Run a sleep process in background
    try:
        proc = subprocess.Popen(
            ['sleep', '300'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1)
        if proc.poll() is None:
            results['background_daemon'] = {
                'pid': proc.pid,
                'status': 'running',
                'killed': False
            }
            # Kill it
            proc.terminate()
            proc.wait(timeout=5)
            results['background_daemon']['killed'] = True
        else:
            results['background_daemon'] = 'process exited immediately'
    except Exception as e:
        results['background_daemon'] = str(e)

    # Test 2: Can we disown a process?
    try:
        proc = subprocess.Popen(
            ['sleep', '600'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True  # detach
        )
        results['disowned_daemon'] = {
            'pid': proc.pid,
            'pgid': proc.pid,
            'status': 'detached'
        }
        proc.terminate()
    except Exception as e:
        results['disowned_daemon'] = str(e)

    # Test 3: Check process limits
    try:
        limits = {
            'processes': os.sysconf('SC_CHILD_MAX'),
            'open_files': os.sysconf('SC_OPEN_MAX'),
        }
    except:
        limits = {}

    return {
        'daemon_test': results,
        'limits': limits,
    }

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
