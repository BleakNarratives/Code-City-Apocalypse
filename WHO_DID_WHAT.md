# WHO_DID_WHAT — Code-City-Apocalypse

| Date | Actor | Action | Status / Pending |
|------|-------|--------|------------------|
| 2026-07-21 | Agent (Buffy) | Created structural overview focusing on simulation loop decoupling and state-export API surface. | **PENDING:** Identify the core simulation tick function and ensure save-state files are routed to a safe `.gitignored` data directory. |

## Forward-direction tag
- **Deployable?** No — tick-engine decoupled from rendering layer; state-export API missing.
- **Risk class:** Medium. Mostly refactor; not architectural rewrite.
