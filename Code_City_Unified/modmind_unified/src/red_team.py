# Author: BleakNarratives
# File: red_team.py
# Path: ~/Code_City_Unified/modmind_unified/src/red_team.py
import socket
import json
import os
from datetime import datetime

class RedTeamScanner:
    def __init__(self, target, ports):
        self.target = target
        self.ports = ports
        self.results = []

    def scan(self):
        print(f"[RedTeam] Scanning {self.target} on {len(self.ports)} ports...")
        for port in self.ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((self.target, port))
                    banner = self._grab_banner(s, port)
                    self.results.append({
                        "port": port, "status": "open",
                        "banner": banner, "timestamp": datetime.now().isoformat()
                    })
                    print(f"  [OPEN]   :{port} → {banner[:60]}")
            except Exception:
                self.results.append({
                    "port": port, "status": "closed",
                    "timestamp": datetime.now().isoformat()
                })

    def _grab_banner(self, s, port):
        try:
            payload = b"HEAD / HTTP/1.0\r\n\r\n" if port in [80, 443] else b"Hello\r\n"
            s.send(payload)
            return s.recv(1024).decode(errors="replace").strip()
        except Exception:
            return "No banner"

    def save_results(self, output_dir="data/scan_results"):
        os.makedirs(output_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"{output_dir}/scan_{self.target}_{ts}.json"
        with open(path, "w") as f:
            json.dump(self.results, f, indent=2)
        print(f"[RedTeam] Results saved → {path}")
        return path
