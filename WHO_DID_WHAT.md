# WHO_DID_WHAT — Code-City-Apocalypse

| Date | Actor | Action | Status / Pending |
|------|-------|--------|------------------|
| 2026-07-21 | Agent (Buffy) | Created structural overview focusing on simulation loop decoupling and state-export API surface. | **PENDING:** Identify the core simulation tick function and ensure save-state files are routed to a safe `.gitignored` data directory. |

## 2026-08-26 — Buffy — Crash arena provenance audit

- Verified the claimed paths instead of trusting the handoff: the Freebuff
  doctor is report-only and does not launch Code City or the MemGuard arena.
  Code City's `crash_feeder.py` independently reads dmesg, vmstat, cgroup,
  journalctl, and `/proc`; it POSTs to `code_city_api.py` `/crash`. MemGuard's
  `tests/arena_round.sh` is a separate memory-pressure harness.
- Found the real persistence gap: Code City active monsters and spawn history
  were process-memory only, while MemGuard's ledger was durable but unrelated.
- Added an explicit crash ledger to `crash_feeder.py` with stable event IDs,
  append-only observation/delivery records, restart-safe delivery deduplication,
  and an opt-in `--include-memguard` adapter that preserves availability,
  PSI, PID, RSS, command, and source telemetry.
- Added `tests/test_crash_feeder.py`: stable IDs, no replay after restart, and
  MemGuard provenance tests pass 3/3.
- Added `../RootBase/EVIDENCE_SPINE.md` as the cross-project persistence map.
  It defines the ownership chain without creating another daemon or database.
- Remaining deliberate limitation: Code City active city state is still
  volatile. Durable evidence and rendered state are now explicitly separated.

## Forward-direction tag
- **Deployable?** No — tick-engine decoupled from rendering layer; state-export API missing.
- **Risk class:** Medium. Mostly refactor; not architectural rewrite.
