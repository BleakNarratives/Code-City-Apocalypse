# Code-City-Apocalypse

## What is this?
A dynamic city simulation or agent-based environment. This project likely deals
with systemic state management, grid/node logic, and simulation loops.

## What's the entry point?
Search for simulation runners like `sim.py`, `city_loop.py`, or a main
execution block that ticks the simulation forward. If there are data files
(JSON / CSV), those represent the initial map / world state.

## Forward Direction & Deployable Status
**Status: Alpha Prototype**

To make this deployable, the simulation tick logic must be decoupled from the
rendering logic. Forward development should focus on establishing a clear
state-export mechanism (e.g. outputting the city state as JSON per tick) so
that external UIs or analytical dashboards can consume the API without stalling
the core game loop.

See also `~/bleaknarratives/INVENTORY.md` and `CROSS_DEVICE_MERGE_PLAN.md`.

---

*Credit: Initial analysis and doc scaffold by Agent (Buffy / Freebuff) — 2026-07-21 un-attended doc-pass. Pending: identify the core simulation tick function and ensure save-state files are routed to a safe `.gitignored` data directory.*
