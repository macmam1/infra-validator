#!/usr/bin/env python3
"""Network check — DNS, outbound, port binding."""
import socket
import json
import subprocess
import urllib.request

def check_dns():
    """Check DNS resolution."""
    try:
        socket.gethostbyname('google.com')
        return True
    except:
        return False

def check_outbound():
    """Check outbound internet access."""
    urls = [
        'https://1.1.1.1/cdn-cgi/trace',
        'https://api.github.com/zen',
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url)
            resp = urllib.request.urlopen(req, timeout=10)
            return True
        except:
            continue
    return False

def check_port_bind(port=8080):
    """Check if we can bind to a port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(1)
        s.close()
        return True
    except Exception as e:
        return str(e)

def check_tcp_udp():
    """Check TCP and UDP availability."""
    results = {}
    # TCP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        results['tcp'] = True
    except Exception as e:
        results['tcp'] = str(e)

    # UDP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('0.0.0.0', 0))
        port = s.getsockname()[1]
        s.close()
        results['udp'] = True
    except Exception as e:
        results['udp'] = str(e)

    return results

def check():
    return {
        "dns": check_dns(),
        "outbound_internet": check_outbound(),
        "port_bind": check_port_bind(),
        "tcp_udp": check_tcp_udp(),
    }

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
