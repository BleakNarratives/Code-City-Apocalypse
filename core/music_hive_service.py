
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: pathlib, sqlite3
# ROLE: MusicHiveService class module
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

import sqlite3
from pathlib import Path

# Path to the persistent whorl state
WHORL_DB = Path.home() / ".whorl" / "whorl.db"

class MusicHiveService:
    def __init__(self):
        self.db_path = WHORL_DB

    def get_state(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT current_key, current_tempo, active_scale, active_mode FROM music_hive ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "key": row[0],
                "tempo": row[1],
                "scale": row[2],
                "mode": row[3]
            }
        return None

    def update_state(self, key, tempo, scale, mode):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO music_hive (current_key, current_tempo, active_scale, active_mode) VALUES (?, ?, ?, ?)",
            (key, tempo, scale, mode)
        )
        conn.commit()
        conn.close()
