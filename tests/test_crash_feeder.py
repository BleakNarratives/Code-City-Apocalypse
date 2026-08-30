#!/usr/bin/env python3
"""Tests for the explicit crash-to-Code-City evidence boundary."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from crash_feeder import CrashEvent, CrashFeeder, CrashLedger


class CrashFeederTests(unittest.TestCase):
    def test_event_id_is_stable_across_instances(self) -> None:
        kwargs = {
            "crash_type": "segfault",
            "source": "dmesg",
            "raw_line": "segfault in worker",
            "target_file": "worker.py",
        }
        self.assertEqual(CrashEvent(**kwargs).event_id, CrashEvent(**kwargs).event_id)

    def test_delivery_is_not_replayed_after_restart(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger_path = Path(tmp) / "crash_events.jsonl"
            event = CrashEvent(
                crash_type="oom_kill",
                source="memguard",
                raw_line="controlled sacrifice pid=42",
                target_file="payment-engine",
            )

            first = CrashFeeder(
                city_url="http://127.0.0.1:9/unreachable",
                ledger_path=ledger_path,
            )
            first.ledger.record_event(event)
            first.ledger.record_delivery(event, True)

            second = CrashFeeder(
                city_url="http://127.0.0.1:9/unreachable",
                ledger_path=ledger_path,
            )
            calls = []
            second.feed_to_city = lambda candidate: calls.append(candidate.event_id) or True

            self.assertEqual(second.feed_batch([event]), 0)
            self.assertEqual(calls, [])
            records = [json.loads(line) for line in ledger_path.read_text().splitlines()]
            self.assertEqual(len(records), 2)
            self.assertTrue(records[-1]["fed"])

    def test_memguard_adapter_is_opt_in_and_preserves_telemetry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            memguard_path = Path(tmp) / "events.jsonl"
            memguard_path.write_text(json.dumps({
                "ts": "2026-08-26T01:00:00+00:00",
                "event": "controlled_sacrifice",
                "avail_mb": 319,
                "psi_some_avg10": 1.66,
                "detail": {
                    "pid": 42,
                    "rss_mb": 17,
                    "cmd": "payment-engine",
                },
            }) + "\n")

            feeder = CrashFeeder(
                ledger_path=Path(tmp) / "crash_events.jsonl",
                include_memguard=True,
                memguard_ledger=memguard_path,
            )
            events = feeder.read_memguard_ledger()

            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].source, "memguard")
            self.assertEqual(events[0].metadata["avail_mb"], 319)
            self.assertEqual(events[0].metadata["psi_some_avg10"], 1.66)
            self.assertIn("payment-engine", events[0].message)


if __name__ == "__main__":
    unittest.main()
