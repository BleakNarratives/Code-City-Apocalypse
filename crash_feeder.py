#!/usr/bin/env python3
"""
crash_feeder.py — System crash monitor that feeds terminal disasters into Code City.

Watches dmesg, journalctl, /proc/vmstat, and OOM reaper logs for crash events.
Each crash spawns a monster in the Code City arena via the crash API.

No heavy deps — pure stdlib. Runs as a background daemon on Crostini/Chromebook.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─── Configuration ────────────────────────────────────────────────

CITY_API_URL = os.getenv("CRASH_FEED_CITY_URL", "http://127.0.0.1:8765/crash")
POLL_INTERVAL = int(os.getenv("CRASH_FEED_POLL", "5"))  # seconds
MAX_CRASHES_PER_CYCLE = int(os.getenv("CRASH_FEED_MAX_PER_CYCLE", "3"))
DMESG_MARKER_FILE = Path(os.path.expanduser("~/.crash_feeder_dmesg_pos"))
CRASH_LEDGER = Path(os.path.expanduser(
    os.getenv("CRASH_FEED_LEDGER", "~/MikeySwarm/logs/code_city/crash_events.jsonl")
))
MEMGUARD_LEDGER = Path(os.path.expanduser(
    os.getenv("CRASH_FEED_MEMGUARD_LEDGER", "~/MikeySwarm/logs/memguard/events.jsonl")
))


@dataclass
class CrashEvent:
    """A single system crash event ready for monster spawning."""
    crash_type: str
    source: str                     # "dmesg" | "journalctl" | "vmstat" | "cgroup"
    raw_line: str
    timestamp: str = ""
    severity: int = 3
    monster_type: str = "Signal Reaper"
    monster_symbol: str = "💀"
    target_file: str = ""           # best guess at affected file
    message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now(timezone.utc).isoformat()

    @property
    def event_id(self) -> str:
        """Return a stable identity so restarts cannot replay fed events."""
        raw = "|".join((self.source, self.crash_type, self.target_file, self.raw_line))
        return hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()[:24]


class CrashLedger:
    """Append-only evidence and delivery ledger for crash-to-monster events."""

    def __init__(self, path: Path = CRASH_LEDGER):
        self.path = Path(path)
        self._latest: Dict[str, Dict[str, Any]] = {}
        self._load()

    def _load(self) -> None:
        try:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                record = json.loads(line)
                event_id = record.get("event_id")
                if event_id:
                    self._latest[event_id] = {
                        **self._latest.get(event_id, {}),
                        **record,
                    }
        except (OSError, ValueError):
            return

    def _append(self, record: Dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        event_id = record["event_id"]
        self._latest[event_id] = {
            **self._latest.get(event_id, {}),
            **record,
        }

    def record_event(self, event: CrashEvent) -> None:
        """Record a newly observed event unless its identity is already known."""
        if event.event_id in self._latest:
            return
        self._append({
            "kind": "crash_event",
            "event_id": event.event_id,
            "fed": False,
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "event": asdict(event),
        })

    def record_delivery(self, event: CrashEvent, fed: bool) -> None:
        """Record the latest delivery state without rewriting prior evidence."""
        previous = self._latest.get(event.event_id, {})
        self._append({
            "kind": "delivery",
            "event_id": event.event_id,
            "fed": fed,
            "attempted_at": datetime.now(timezone.utc).isoformat(),
            "attempts": int(previous.get("attempts", 0)) + 1,
        })

    def is_delivered(self, event: CrashEvent) -> bool:
        record = self._latest.get(event.event_id, {})
        return bool(record.get("fed"))

    def pending_events(self) -> List[CrashEvent]:
        """Reconstruct events that were observed but not delivered."""
        pending = []
        for record in self._latest.values():
            if record.get("fed"):
                continue
            event_data = record.get("event")
            if event_data:
                pending.append(CrashEvent(**event_data))
        return pending


class CrashFeeder:
    """
    Multi-source system crash monitor.

    Sources (in order of reliability on Crostini):
    1. dmesg — kernel ring buffer (OOM, segfault, kernel panics)
    2. /proc/vmstat — memory pressure counters
    3. cgroup memory events — container OOM detection
    4. journalctl — user-space crash logs (if available)
    """

    def __init__(
        self,
        city_url: str = CITY_API_URL,
        *,
        ledger_path: Path = CRASH_LEDGER,
        include_memguard: bool = False,
        memguard_ledger: Path = MEMGUARD_LEDGER,
    ):
        self.city_url = city_url
        self.seen_hashes: set = set()
        self.last_dmesg_pos = self._load_dmesg_pos()
        self.crash_count = 0
        self.ledger = CrashLedger(ledger_path)
        self.include_memguard = include_memguard
        self.memguard_ledger = Path(memguard_ledger)
        # Monotonic counters only fire on meaningful increases, otherwise the
        # vmstat alloc_stall/oom_kill counters (which never decrease) would
        # spawn a monster on every poll forever. Thresholds: alloc_stall re-
        # fires only after +50 since last emission; oom_kill only on increase.
        self._vmstat_watermarks: Dict[str, int] = {}

    # ── DMESG ──────────────────────────────────────────────────

    def _load_dmesg_pos(self) -> int:
        """Load last dmesg read position to avoid re-reading."""
        try:
            return int(DMESG_MARKER_FILE.read_text().strip())
        except Exception:
            return 0

    def _save_dmesg_pos(self, pos: int) -> None:
        DMESG_MARKER_FILE.write_text(str(pos))

    def read_dmesg(self) -> List[CrashEvent]:
        """
        Read new dmesg lines since last poll.
        On Crostini/Chromebook, dmesg may require sudo or be restricted.
        Falls back gracefully.
        """
        events = []
        try:
            result = subprocess.run(
                ["dmesg", "--kernel", "--level=emerg,alert,crit,err,warn"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                return events

            lines = result.stdout.strip().split("\n")
            for line in lines[self.last_dmesg_pos:]:
                event = self._parse_dmesg_line(line)
                if event:
                    events.append(event)

            self._save_dmesg_pos(len(lines))
        except FileNotFoundError:
            pass  # dmesg not available
        except Exception:
            pass

        return events

    def _parse_dmesg_line(self, line: str) -> Optional[CrashEvent]:
        """Parse a dmesg line into a CrashEvent if it's a crash indicator."""
        crash_patterns: List[Tuple[str, str, int, str, str, re.Pattern]] = [
            # (crash_type, monster_type, severity, symbol, regex, description_template)
            ("oom_kill", "Memory Wraith", 5, "🧟",
             re.compile(r"Out of memory.*process\s+(\S+)", re.IGNORECASE),
             "OOM killer nuked process: {match} — system memory exhausted"),
            ("segfault", "Segmentation Specter", 4, "👻",
             re.compile(r"segfault.*in\s+(\S+)", re.IGNORECASE),
             "Segfault in {match} — memory access violation"),
            ("kernel_panic", "Kernel Kraken", 5, "🐙",
             re.compile(r"Kernel panic", re.IGNORECASE),
             "Kernel panic — system is on fire"),
            ("oom_reaper", "Reaper Wraith", 4, "☠️",
             re.compile(r"oom_reaper.*reaped\s+(\S+)", re.IGNORECASE),
             "OOM reaper harvested {match}"),
            ("protection_fault", "Guard Gargoyle", 4, "🗿",
             re.compile(r"protection fault.*in\s+(\S+)", re.IGNORECASE),
             "General protection fault in {match}"),
            ("bug", "Kernel Gremlin", 3, "👹",
             re.compile(r"BUG:.*at\s+(\S+)", re.IGNORECASE),
             "Kernel BUG at {match}"),
            ("null_pointer", "Null Phantom", 3, "🫥",
             re.compile(r"NULL pointer dereference.*in\s+(\S+)", re.IGNORECASE),
             "NULL pointer dereference in {match}"),
        ]

        for crash_type, monster, severity, symbol, pattern, template in crash_patterns:
            m = pattern.search(line)
            if m:
                match_val = m.group(1) if m.groups() else "unknown"
                return CrashEvent(
                    crash_type=crash_type,
                    source="dmesg",
                    raw_line=line,
                    severity=severity,
                    monster_type=monster,
                    monster_symbol=symbol,
                    target_file=match_val,
                    message=template.format(match=match_val),
                )

        return None

    # ── VMSTAT (memory pressure) ───────────────────────────────

    def read_vmstat(self) -> List[CrashEvent]:
        """Read /proc/vmstat for memory pressure indicators."""
        events = []
        try:
            vmstat = Path("/proc/vmstat").read_text()
            metrics = {}
            for line in vmstat.strip().split("\n"):
                if " " in line:
                    k, v = line.split(None, 1)
                    try:
                        metrics[k] = int(v)
                    except ValueError:
                        pass

            # OOM count (fires only when the counter increases)
            oom_kill = metrics.get("oom_kill", 0)
            if oom_kill > self._vmstat_watermarks.get("oom_kill", 0):
                self._vmstat_watermarks["oom_kill"] = oom_kill
                if oom_kill > 0:
                    events.append(CrashEvent(
                        crash_type="oom_pressure",
                        source="vmstat",
                        raw_line=f"oom_kill={oom_kill}",
                        severity=min(5, oom_kill),
                        monster_type="Pressure Phantom",
                        monster_symbol="💨",
                        message=f"Memory pressure: {oom_kill} OOM kills recorded since boot",
                        metadata={"oom_kill_count": oom_kill},
                    ))

            # Page allocation failures (fires only when +50 past last emission)
            alloc_stall = metrics.get("allocstall_normal", 0) + metrics.get("allocstall_movable", 0)
            last = self._vmstat_watermarks.get("alloc_stall", 0)
            if alloc_stall > 100 and alloc_stall >= last + 50:
                self._vmstat_watermarks["alloc_stall"] = alloc_stall
                events.append(CrashEvent(
                    crash_type="alloc_stall",
                    source="vmstat",
                    raw_line=f"allocstall={alloc_stall}",
                    severity=3,
                    monster_type="Alloc Imp",
                    monster_symbol="👹",
                    message=f"High allocation stalls: {alloc_stall} — memory fragmentation",
                    metadata={"allocstall": alloc_stall},
                ))

        except Exception:
            pass

        return events

    # ── CGROUP (container OOM) ─────────────────────────────────

    def read_cgroup_events(self) -> List[CrashEvent]:
        """Check cgroup memory events for container-level OOM."""
        events = []
        cgroup_paths = [
            "/sys/fs/cgroup/memory/memory.events",     # cgroup v1
            "/sys/fs/cgroup/memory.events",             # cgroup v2
        ]

        for path_str in cgroup_paths:
            p = Path(path_str)
            if not p.exists():
                continue
            try:
                content = p.read_text()
                for line in content.strip().split("\n"):
                    if "oom" in line.lower() and " " in line:
                        key, val = line.strip().split(None, 1)
                        if int(val) > 0:
                            events.append(CrashEvent(
                                crash_type="cgroup_oom",
                                source="cgroup",
                                raw_line=line.strip(),
                                severity=4,
                                monster_type="Container Kraken",
                                monster_symbol="🐙",
                                message=f"Cgroup OOM event: {key}={val} — container memory limit hit",
                                metadata={"cgroup_key": key, "cgroup_value": int(val)},
                            ))
            except Exception:
                continue

        return events

    # ── JOURNALCTL ─────────────────────────────────────────────

    def read_journalctl(self) -> List[CrashEvent]:
        """Read recent crash events from journalctl (if available)."""
        events = []
        try:
            result = subprocess.run(
                ["journalctl", "--no-pager", "-p", "0..3", "--since", "1 minute ago", "-n", "20"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                return events

            for line in result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                # Look for crash indicators
                if re.search(r"(segfault|SIGSEGV|SIGABRT|core dumped|crashed|killed|OOM)", line, re.IGNORECASE):
                    # Determine crash type
                    if "oom" in line.lower() or "out of memory" in line.lower():
                        crash_type, monster, sev, sym = "oom_journal", "Memory Wraith", 5, "🧟"
                    elif "segfault" in line.lower() or "sigsegv" in line.lower():
                        crash_type, monster, sev, sym = "segfault_journal", "Segmentation Specter", 4, "👻"
                    elif "sigabrt" in line.lower():
                        crash_type, monster, sev, sym = "abort_journal", "Abort Golem", 3, "🗿"
                    elif "core dumped" in line.lower():
                        crash_type, monster, sev, sym = "core_dump", "Core Specter", 3, "🫥"
                    else:
                        crash_type, monster, sev, sym = "process_death", "Signal Reaper", 2, "💀"

                    events.append(CrashEvent(
                        crash_type=crash_type,
                        source="journalctl",
                        raw_line=line,
                        severity=sev,
                        monster_type=monster,
                        monster_symbol=sym,
                        message=line[:200],
                    ))

        except FileNotFoundError:
            pass
        except Exception:
            pass

        return events

    # ── Process watch (check our own processes) ────────────────

    def read_proc_self(self) -> List[CrashEvent]:
        """Check /proc/self/status for our own memory pressure."""
        events = []
        try:
            status = Path("/proc/self/status").read_text()
            for line in status.split("\n"):
                if line.startswith("VmRSS:"):
                    try:
                        rss_kb = int(line.split()[1])
                        rss_mb = rss_kb // 1024
                        if rss_mb > 800:  # Over 800MB RSS
                            events.append(CrashEvent(
                                crash_type="self_memory_pressure",
                                source="proc",
                                raw_line=line.strip(),
                                severity=2,
                                monster_type="Bloat Beast",
                                monster_symbol="🐡",
                                message=f"Self RSS at {rss_mb}MB — approaching OOM territory",
                                metadata={"rss_mb": rss_mb},
                            ))
                    except (IndexError, ValueError):
                        pass
        except Exception:
            pass
        return events

    # ── MemGuard adapter ───────────────────────────────────────

    def read_memguard_ledger(self) -> List[CrashEvent]:
        """Opt-in adapter: translate MemGuard casualties into crash events."""
        if not self.memguard_ledger.exists():
            return []
        events = []
        try:
            for line in self.memguard_ledger.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                record = json.loads(line)
                if record.get("event") != "controlled_sacrifice":
                    continue
                detail = record.get("detail", {})
                command = str(detail.get("cmd", "unknown process"))
                events.append(CrashEvent(
                    crash_type="memguard_controlled_sacrifice",
                    source="memguard",
                    raw_line=line,
                    timestamp=record.get("ts", ""),
                    severity=4,
                    monster_type="Controlled Sacrifice Wraith",
                    monster_symbol="☠",
                    target_file=command,
                    message=(
                        f"MemGuard terminated expendable process {command[:160]} "
                        f"at {record.get('avail_mb', '?')}MB available"
                    ),
                    metadata={
                        "memguard_event": record.get("event"),
                        "avail_mb": record.get("avail_mb"),
                        "psi_some_avg10": record.get("psi_some_avg10"),
                        "detail": detail,
                    },
                ))
        except (OSError, ValueError):
            return []
        return events

    # ── Aggregate and deduplicate ──────────────────────────────

    def collect_all_crashes(self) -> List[CrashEvent]:
        """Collect crash events from all available sources."""
        all_events = []

        source_fns = [
            self.read_dmesg,
            self.read_vmstat,
            self.read_cgroup_events,
            self.read_journalctl,
            self.read_proc_self,
        ]
        if self.include_memguard:
            source_fns.append(self.read_memguard_ledger)

        for source_fn in source_fns:
            try:
                events = source_fn()
                all_events.extend(events)
            except Exception:
                continue

        # Dedup within this cycle (local), across cycles (durable ledger), and
        # drop anything already delivered so the per-cycle cap applies to
        # PENDING events only. A stable head of already-fed events must not
        # starve the backlog (the 2026-08-26 daemon bug: a persistent in-memory
        # `seen_hashes` gate re-skipped every pending event after the first
        # cycle, so the city never ingested the backlog).
        unique = []
        seen_this_cycle = set()
        for e in all_events:
            key = e.event_id
            if key in seen_this_cycle:
                continue
            seen_this_cycle.add(key)
            self.seen_hashes.add(key)  # cumulative "ever detected" count
            self.ledger.record_event(e)  # durable dedup (no-op if known)
            if self.ledger.is_delivered(e):
                continue
            unique.append(e)

        # Prune the cumulative set (keep last 1000).
        if len(self.seen_hashes) > 1000:
            self.seen_hashes = set(list(self.seen_hashes)[-500:])

        return unique[:MAX_CRASHES_PER_CYCLE]

    # ── Feed to City API ───────────────────────────────────────

    def feed_to_city(self, event: CrashEvent) -> bool:
        """POST a crash event to the Code City crash API."""
        try:
            data = json.dumps({
                "error_type": event.crash_type,
                "file_path": event.target_file or f"/proc/{event.source}/{event.crash_type}",
                "error_message": event.message,
                "severity": event.severity,
                "monster_type": event.monster_type,
                "monster_symbol": event.monster_symbol,
                "source": event.source,
                "timestamp": event.timestamp,
            }).encode("utf-8")

            req = urllib.request.Request(
                self.city_url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status in (200, 201):
                    self.crash_count += 1
                    return True

        except urllib.error.URLError:
            pass  # City API not running — that's fine, don't crash the feeder
        except Exception:
            pass

        return False

    def feed_batch(self, events: List[CrashEvent]) -> int:
        """Feed a batch of events to Code City. Returns count of successful feeds."""
        fed = 0
        for event in events:
            if self.ledger.is_delivered(event):
                continue
            delivered = self.feed_to_city(event)
            self.ledger.record_delivery(event, delivered)
            if delivered:
                fed += 1
                print(f"  {event.monster_symbol} {event.monster_type}: {event.message[:100]}")
        return fed

    # ── Main loop ──────────────────────────────────────────────

    def run_forever(self) -> None:
        """
        Main daemon loop. Polls all sources, feeds crashes to Code City.
        Press Ctrl+C to stop.
        """
        print("═══ CRASH FEEDER ═══")
        print(f"Target: {self.city_url}")
        print(f"Poll interval: {POLL_INTERVAL}s")
        print(f"Max crashes/cycle: {MAX_CRASHES_PER_CYCLE}")
        print(f"Crash sources: dmesg, vmstat, cgroup, journalctl, /proc")
        print("Monitoring for system disasters...")
        print()

        try:
            while True:
                events = self.collect_all_crashes()

                if events:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {len(events)} crash event(s) detected:")
                    fed = self.feed_batch(events)
                    if fed > 0:
                        print(f"  → {fed} monster(s) spawned in Code City")
                    else:
                        print(f"  → City API unreachable — events logged locally")

                time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print(f"\n═══ CRASH FEEDER STOPPED ═══")
            print(f"Total crashes detected: {len(self.seen_hashes)}")
            print(f"Monsters spawned: {self.crash_count}")


# ─── CLI ──────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="System crash monitor → Code City monster spawner",
    )
    parser.add_argument("--url", default=CITY_API_URL,
                        help=f"Code City crash API URL (default: {CITY_API_URL})")
    parser.add_argument("--poll", type=int, default=POLL_INTERVAL,
                        help=f"Poll interval in seconds (default: {POLL_INTERVAL})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Detect crashes but don't send to API")
    parser.add_argument("--include-memguard", action="store_true",
                        help="Opt in to MemGuard controlled-sacrifice events")
    parser.add_argument("--ledger", type=Path, default=CRASH_LEDGER,
                        help=f"Crash event ledger (default: {CRASH_LEDGER})")
    parser.add_argument("--once", action="store_true",
                        help="Run one scan and exit")

    args = parser.parse_args()

    feeder = CrashFeeder(
        city_url=args.url,
        ledger_path=args.ledger,
        include_memguard=args.include_memguard,
    )

    if args.once:
        events = feeder.collect_all_crashes()
        if events:
            print(f"Detected {len(events)} crash event(s):")
            for e in events:
                print(f"  {e.monster_symbol} [{e.crash_type}] {e.message}")
            if not args.dry_run:
                fed = feeder.feed_batch(events)
                print(f"Spawned {fed} monsters")
        else:
            print("No crashes detected. System is healthy.")
        return

    if args.dry_run:
        print("DRY RUN MODE — detecting but not sending")
        feeder.city_url = "http://127.0.0.1:9/nope"  # guaranteed unreachable

    feeder.run_forever()


if __name__ == "__main__":
    main()