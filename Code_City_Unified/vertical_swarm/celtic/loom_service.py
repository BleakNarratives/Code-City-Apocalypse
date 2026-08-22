#!/usr/bin/env python3
"""
Creates loom_state.db and provides REST API for fibers.
"""
import json, sqlite3
from flask import Flask, request, jsonify
from fiber_core import DataFiber
from celtic_crypto import CelticDataLoom

DB_PATH = "/home/bleaknarratives/Code-City-Apocalypse/loom_state.db"
app = Flask(__name__)
loom = CelticDataLoom()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS fibers (
        fiber_id TEXT PRIMARY KEY,
        owner_id TEXT,
        content_hash TEXT,
        fiber_type TEXT,
        raw_data TEXT,
        timestamp TEXT
    )""")
    conn.commit(); conn.close()

@app.route("/status")
def status():
    return jsonify(loom.get_collective_status())

if __name__ == "__main__":
    init_db()
    print("💾 SQLite ready at", DB_PATH)
    app.run(host="0.0.0.0", port=5050)
