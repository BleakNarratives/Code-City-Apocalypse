#!/usr/bin/env python3
"""
crash_monster.py — Crash type → Code City disaster/monster mapper.

Classifies crash events, assigns monster types, severity, symbols, and
optionally uses the ox CLI to generate theatrical disaster descriptions.

Can run standalone (reads crash events from stdin) or imported as a library.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ─── Crash type → Monster mapping ────────────────────────────────

@dataclass
class MonsterTemplate:
    """A monster type mapped to a crash pattern."""
    crash_type: str
    monster_name: str
    symbol: str
    severity: int                 # 1-5
    keywords: List[str]           # trigger keywords
    disaster_type: str            # maps to CodeCityApocalypse disaster_types
    flavor_text: str              # default description template
    attack_style: str = "SMASH"   # SMASH, CHOMP, SLASH, DRAIN, BOMB, HAUNT

    def generate_message(self, crash_line: str, process_name: str = "") -> str:
        """Build a disaster message from the crash data."""
        name = process_name or "unknown process"
        return self.flavor_text.format(name=name, line=crash_line[:100])


# The canonical crash-to-monster bestiary
MONSTER_BESTIARY: List[MonsterTemplate] = [
    MonsterTemplate(
        crash_type="oom_kill",
        monster_name="Memory Wraith",
        symbol="🧟",
        severity=5,
        keywords=["oom", "out of memory", "oom-killer", "killed process", "invoked oom"],
        disaster_type="memory_error",
        flavor_text="OOM Killer devoured {name} — {line}",
        attack_style="DRAIN",
    ),
    MonsterTemplate(
        crash_type="segfault",
        monster_name="Segmentation Specter",
        symbol="👻",
        severity=4,
        keywords=["segfault", "segmentation fault", "SIGSEGV", "core dumped"],
        disaster_type="runtime_error",
        flavor_text="Segfault ghost-haunted {name} at address {line}",
        attack_style="HAUNT",
    ),
    MonsterTemplate(
        crash_type="kernel_panic",
        monster_name="Kernel Kraken",
        symbol="🐙",
        severity=5,
        keywords=["kernel panic", "not syncing", "end trace"],
        disaster_type="memory_error",
        flavor_text="KERNEL PANIC — the Kernel Kraken rises! {line}",
        attack_style="SMASH",
    ),
    MonsterTemplate(
        crash_type="sigabrt",
        monster_name="Abort Golem",
        symbol="🗿",
        severity=3,
        keywords=["SIGABRT", "aborted", "abort", "assertion failed"],
        disaster_type="logic_error",
        flavor_text="Abort Golem crushed {name}: {line}",
        attack_style="SMASH",
    ),
    MonsterTemplate(
        crash_type="sigkill",
        monster_name="Reaper Scythe",
        symbol="💀",
        severity=4,
        keywords=["SIGKILL", "killed", "terminated"],
        disaster_type="runtime_error",
        flavor_text="Reaper's scythe harvested {name}: {line}",
        attack_style="SLASH",
    ),
    MonsterTemplate(
        crash_type="sigbus",
        monster_name="Bus Basilisk",
        symbol="🐍",
        severity=4,
        keywords=["SIGBUS", "bus error", "alignment fault"],
        disaster_type="runtime_error",
        flavor_text="Bus Basilisk petrified {name}: {line}",
        attack_style="HAUNT",
    ),
    MonsterTemplate(
        crash_type="sigpipe",
        monster_name="Pipe Phantom",
        symbol="👻",
        severity=2,
        keywords=["SIGPIPE", "broken pipe"],
        disaster_type="logic_error",
        flavor_text="Pipe Phantom broke connection to {name}",
        attack_style="DRAIN",
    ),
    MonsterTemplate(
        crash_type="null_pointer",
        monster_name="Null Phantom",
        symbol="🫥",
        severity=3,
        keywords=["null pointer", "NULL pointer", "dereference"],
        disaster_type="runtime_error",
        flavor_text="Null Phantom dereferenced {name} into the void",
        attack_style="HAUNT",
    ),
    MonsterTemplate(
        crash_type="memory_pressure",
        monster_name="Pressure Phantom",
        symbol="💨",
        severity=3,
        keywords=["memory pressure", "allocstall", "page allocation failure"],
        disaster_type="memory_error",
        flavor_text="Memory pressure crushing {name}: {line}",
        attack_style="DRAIN",
    ),
    MonsterTemplate(
        crash_type="disk_error",
        monster_name="Disk Demon",
        symbol="👹",
        severity=3,
        keywords=["I/O error", "disk error", "filesystem", "read-only"],
        disaster_type="runtime_error",
        flavor_text="Disk Demon corrupted {name}: {line}",
        attack_style="BOMB",
    ),
    MonsterTemplate(
        crash_type="network_timeout",
        monster_name="Lag Wraith",
        symbol="🌫️",
        severity=2,
        keywords=["timeout", "connection refused", "network unreachable", "no route"],
        disaster_type="logic_error",
        flavor_text="Lag Wraith slowed {name} to a crawl",
        attack_style="DRAIN",
    ),
    MonsterTemplate(
        crash_type="cpu_throttle",
        monster_name="Throttle Troll",
        symbol="👺",
        severity=2,
        keywords=["throttl", "temperature", "overheat"],
        disaster_type="logic_error",
        flavor_text="Throttle Troll slammed the brakes on {name}",
        attack_style="SMASH",
    ),
    MonsterTemplate(
        crash_type="swap_exhaustion",
        monster_name="Swap Hydra",
        symbol="🐉",
        severity=4,
        keywords=["swap", "swap full", "no swap"],
        disaster_type="memory_error",
        flavor_text="Swap Hydra's heads devoured all memory for {name}",
        attack_style="CHOMP",
    ),
    MonsterTemplate(
        crash_type="unknown_crash",
        monster_name="Chaos Imp",
        symbol="👾",
        severity=3,
        keywords=[],
        disaster_type="runtime_error",
        flavor_text="Chaos Imp rampaged through {name}: {line}",
        attack_style="SMASH",
    ),
]


class CrashClassifier:
    """Classify crash events and map them to Code City monsters."""

    def __init__(self, bestiary: Optional[List[MonsterTemplate]] = None):
        self.bestiary = bestiary or MONSTER_BESTIARY
        self.ox_bin = os.path.expanduser("~/bin/ox")
        self._ox_available: Optional[bool] = None

    def classify(self, crash_text: str, process_name: str = "") -> MonsterTemplate:
        """
        Classify a crash text and return the matching monster template.
        Falls back to Chaos Imp if nothing matches.
        """
        text_lower = crash_text.lower()

        # Score each template by keyword matches
        best_match: Optional[MonsterTemplate] = None
        best_score = 0

        for template in self.bestiary:
            if not template.keywords:
                continue  # skip the catch-all
            score = sum(1 for kw in template.keywords if kw.lower() in text_lower)
            # Boost severity-based priority
            if score > 0:
                score += template.severity * 0.5
            if score > best_score:
                best_score = score
                best_match = template

        return best_match or self.bestiary[-1]  # fallback to Chaos Imp

    def classify_enhanced(self, crash_text: str, process_name: str = ""
                          ) -> Dict[str, Any]:
        """
        Classify and return a full spawn-ready dict with optional ox enhancement.
        """
        template = self.classify(crash_text, process_name)
        message = template.generate_message(crash_text, process_name)

        return {
            "error_type": template.crash_type,
            "error_message": message,
            "severity": template.severity,
            "monster_type": template.monster_name,
            "monster_symbol": template.symbol,
            "disaster_type": template.disaster_type,
            "attack_style": template.attack_style,
        }

    def classify_with_ox_flair(self, crash_text: str, process_name: str = ""
                               ) -> Dict[str, Any]:
        """
        Classify and optionally enhance the disaster description with ox CLI.

        If ox is available and has a key, it generates a more theatrical
        description. Falls back to template-based message if ox is unavailable.
        """
        result = self.classify_enhanced(crash_text, process_name)

        if self.is_ox_available():
            try:
                flair = self._generate_ox_flair(
                    crash_text, result["monster_name"], result["monster_symbol"]
                )
                if flair and "error" not in flair.lower() and len(flair) > 10:
                    result["error_message"] = flair.strip()
                    result["ox_enhanced"] = True
            except Exception:
                result["ox_enhanced"] = False

        return result

    def is_ox_available(self) -> bool:
        """Check if ox CLI is available and has an API key."""
        if self._ox_available is not None:
            return self._ox_available

        if not Path(self.ox_bin).exists():
            self._ox_available = False
            return False

        if not os.getenv("OPENROUTER_API_KEY"):
            # Check ~/.oxrc
            oxrc = Path.home() / ".oxrc"
            if oxrc.exists():
                content = oxrc.read_text()
                if "openrouter_api_key=sk-or-v1" in content:
                    self._ox_available = True
                    return True

        if os.getenv("OPENROUTER_API_KEY"):
            self._ox_available = True
            return True

        self._ox_available = False
        return False

    def _generate_ox_flair(self, crash_text: str, monster_name: str,
                           symbol: str) -> Optional[str]:
        """Use ox CLI to generate a theatrical crash description."""
        prompt = (
            f"A system crash just occurred. Describe it in ONE theatrical sentence "
            f"as if a monster named '{symbol} {monster_name}' attacked the system.\n\n"
            f"Crash details: {crash_text[:300]}\n\n"
            f"Style: dramatic, visual, 20 words max. Just the sentence, nothing else."
        )

        try:
            result = subprocess.run(
                [self.ox_bin, "--no-stream", "--max-tokens", "100",
                 "-t", "0.9", prompt],
                capture_output=True, text=True, timeout=15,
                env={**os.environ},
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass

        return None

    def classify_batch(self, crashes: List[Dict[str, Any]],
                       use_ox: bool = False) -> List[Dict[str, Any]]:
        """Classify a batch of crash events."""
        results = []
        for crash in crashes:
            text = crash.get("raw_line", crash.get("error_message", ""))
            name = crash.get("process_name", crash.get("target_file", ""))

            if use_ox:
                result = self.classify_with_ox_flair(text, name)
            else:
                result = self.classify_enhanced(text, name)

            # Preserve source metadata
            result["source"] = crash.get("source", "unknown")
            result["original_raw_line"] = text[:200]
            results.append(result)

        return results

    def list_bestiary(self) -> List[Dict[str, Any]]:
        """List all available monster types."""
        return [
            {
                "crash_type": t.crash_type,
                "monster": t.monster_name,
                "symbol": t.symbol,
                "severity": t.severity,
                "keywords": t.keywords[:5],
                "attack": t.attack_style,
            }
            for t in self.bestiary
        ]


# ─── Standalone mode: read crashes from stdin ────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Crash → Monster classifier for Code City",
    )
    parser.add_argument("--bestiary", action="store_true",
                        help="List the complete monster bestiary")
    parser.add_argument("--ox-flair", action="store_true",
                        help="Enhance descriptions with ox CLI")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")
    parser.add_argument("crash_text", nargs="*",
                        help="Crash text to classify (or pipe via stdin)")

    args = parser.parse_args()
    classifier = CrashClassifier()

    if args.bestiary:
        if args.json:
            print(json.dumps(classifier.list_bestiary(), indent=2))
        else:
            print("═══ CRASH MONSTER BESTIARY ═══")
            for m in classifier.bestiary:
                print(f"  {m.symbol} {m.monster_name} ({m.crash_type})")
                print(f"    Severity: {m.severity}/5  Attack: {m.attack_style}")
                print(f"    Keywords: {', '.join(m.keywords[:5])}")
                print()
        return

    # Read crash text
    crash_text = " ".join(args.crash_text).strip()
    if not crash_text and not sys.stdin.isatty():
        crash_text = sys.stdin.read().strip()

    if not crash_text:
        parser.print_help()
        sys.exit(1)

    result = classifier.classify_with_ox_flair(crash_text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['monster_symbol']} {result['monster_type']} (severity {result['severity']}/5)")
        print(f"Attack: {result['attack_style']}")
        print(f"Disaster: {result['disaster_type']}")
        print(f"Message: {result['error_message']}")
        if result.get("ox_enhanced"):
            print("(enhanced by ox)")


if __name__ == "__main__":
    main()