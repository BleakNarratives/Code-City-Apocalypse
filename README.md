# Code City Apocalypse

**Red team / blue team wargame — 514 Python files, zero syntax errors.**

A dynamic city simulation where agents compete in a cyberpunk wargame. Red team agents (VIPER, RAVAGE, WRAPPER) attack. Blue team agents (EQUINEX, LIDARR, BASTION) defend. The city evolves through agent interactions.

---

## Agents

### Red Team
| Agent | Role | Specialty |
|-------|------|-----------|
| **VIPER** | Precision | Auger — surgical strikes |
| **RAVAGE** | Brute Force | Overwhelming force |
| **WRAPPER** | UI Mimicry | Social engineering |

### Blue Team
| Agent | Role | Specialty |
|-------|------|-----------|
| **EQUINEX** | ModMind Guardian | System protection |
| **LIDARR** | Topography/Radar | Threat detection |
| **BASTION** | Immutable Rollback | Recovery and defense |

### S-Rank Brown Hat
| Agent | Role |
|-------|------|
| **THE SHIT SHOVELER** | Three named special moves, non-negotiable |

---

## Structure

```
Code_City/                  Core simulation
Code_City_Unified/          Unified agent system
SCOUT_CONTAINER/            Scout and intelligence modules
backend/                    Server infrastructure
frontend/                   UI and visualization
code_tool/                  Code extraction utilities
```

## Stats

- **514 Python files** — 0 syntax errors
- **392 DNA-tagged files** — full lineage tracking
- **51 syntax errors fixed** — all resolved in Sprint Ralphie

## Running

```bash
python3 code_city_apocalypse.py

# Crash-to-monster bridge. MemGuard input is opt-in.
python3 crash_feeder.py --once --dry-run
python3 crash_feeder.py --once --dry-run --include-memguard
```

## Verified Crash Boundary

`start_crash_arena.sh` starts the Code City API and `crash_feeder.py`. The
feeder watches dmesg, vmstat, cgroup events, journalctl, and optionally the
MemGuard ledger. It POSTs translated events to `/crash`.

The Freebuff doctor is not in this path. It is a report-only health shell. The
MemGuard stress arena is also separate: it creates memory pressure for testing
and does not feed Code City. Code City's active monsters are currently
in-memory and disappear when its API restarts.

The feeder now writes an append-only evidence ledger at
`~/MikeySwarm/logs/code_city/crash_events.jsonl`, uses stable event IDs, and
records delivery status so successful monster feeds are not replayed after a
restart. MemGuard translation requires the explicit `--include-memguard` flag.
See `../RootBase/EVIDENCE_SPINE.md` for the cross-project persistence map.

## Status

**Alpha Prototype** — simulation tick logic decoupled from rendering. City state
is exportable as JSON for external dashboards. Crash evidence is persistent at
the feeder boundary; active city state remains volatile.

---

*BleakNarratives // 2026*
