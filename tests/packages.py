#!/usr/bin/env python3
"""Package management check — apt, pip, npm, curl, wget."""
import shutil
import json

def check():
    pkgs = {}
    for pkg in ['apt-get', 'apt', 'pip', 'pip3', 'npm', 'npx', 'curl', 'wget', 'git', 'docker', 'unzip', 'sudo']:
        path = shutil.which(pkg)
        pkgs[pkg] = path if path else None
    return {"package_managers": pkgs}

if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
