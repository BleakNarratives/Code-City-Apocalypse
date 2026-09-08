# ==============================================================================
# SCOUT_CONTAINER / scout_bridge.py
# The staging ground — Code-City's red team deploys Vigil scouts from here.
#
# The arena is where they go to battle. This bridge is the arm that fights:
# it runs a full Vigil scout wargame (signed scouts, geometric bids, PeerWatch
# market, Repugnant register, Theoros reading, Culture mines) against any
# target path and returns structured intel the red team can act on.
#
# Usage (from anywhere in Code-City):
#   from scout_bridge import run_recon, scout_report
#   intel = run_recon("/path/to/target", rounds=3)
#   brief = scout_report(intel)   # condensed operator-facing intel
#
# CLI:
#   python3 scout_bridge.py /path/to/target [rounds]
#
# Modular by design: the bridge only imports Vigil's public surface and
# returns plain dicts — no coupling back into Code-City internals, so the
# scouts can be swapped, upgraded, or self-modified without touching the city.
# ==============================================================================

import json
import os
import sys

# Vigil lives at ~/vigil — the bridge reaches it without polluting the city's
# own imports. If Vigil moves, update this one path (or drop a symlink).
# Both parents are needed: '~' resolves `import vigil.*`, while '~/vigil'
# resolves the bare internal imports (e.g. `from pheromone_store import`).
_VIGIL_HOME = os.path.expanduser("~/vigil")
for _p in (os.path.expanduser("~"), _VIGIL_HOME):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load_wargame():
    """Import ScoutWargame lazily so the bridge degrades to a clear error
    (not a traceback) when Vigil isn't on the box."""
    try:
        from vigil.wargame import ScoutWargame
        return ScoutWargame
    except ImportError as exc:
        raise RuntimeError(
            f"Vigil not importable from {_VIGIL_HOME}: {exc}. "
            f"Run the Vigil setup or fix the path at the top of scout_bridge.py."
        ) from exc


def run_recon(target, rounds=3, deploy_mines=True):
    """Run the scout wargame against a target and return full intel.

    Returns the raw ScoutWargame.play() dict enriched with a summary —
    plain data only, ready to be logged, fed to the red team, or shipped
    to Sakshi.
    """
    if not os.path.isdir(target):
        raise ValueError(f"target is not a directory: {target}")

    ScoutWargame = _load_wargame()
    game = ScoutWargame(target, rounds=rounds)
    result = game.play()

    intel = dict(result)
    intel["target"] = target
    intel["rounds"] = rounds
    intel["summary"] = {
        "red_score": result.get("red_score", 0),
        "blue_score": result.get("blue_score", 0),
        "findings": result.get("findings", 0),
        "executions": result.get("executions", 0),
        "blocks": result.get("blocks", 0),
        "mines_deployed": len(result.get("mines", [])),
        "corrupt_speakers": result.get("corrupt_speakers", 0),
        "theoros_consistent": result.get("theoros_consistent", False),
        "molt_awards": result.get("molt_awards", []),
    }
    return intel


def scout_report(intel):
    """Condense full intel into an operator-facing brief."""
    s = intel.get("summary", {})
    lines = [
        f"TARGET: {intel.get('target')} ({intel.get('rounds')} rounds)",
        f"RED {s.get('red_score')} / BLUE {s.get('blue_score')}",
        f"FINDINGS {s.get('findings')} | EXECUTIONS {s.get('executions')} "
        f"| BLOCKS {s.get('blocks')}",
        f"MINES {s.get('mines_deployed')} | CORRUPT SPEAKERS "
        f"{s.get('corrupt_speakers')} | THEOROS CONSISTENT "
        f"{s.get('theoros_consistent')}",
    ]
    molts = s.get("molt_awards", [])
    if molts:
        lines.append("MOLT AWARDED TO: "
                     + ", ".join(m.get("agent_id", "?") for m in molts))
    brown = intel.get("brown")
    if brown is not None:
        lines.append("BROWN: " + brown.unify_or_get_humped)
    readings = []
    for key in ("reading", "blue_reading"):
        r = intel.get(key)
        if r is not None and hasattr(r, "render"):
            readings.append(r.render())
    return "\n".join(lines) + ("\n" + "\n\n".join(readings) if readings else "")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scout_bridge.py <target_dir> [rounds]")
        sys.exit(1)
    target = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    intel = run_recon(target, rounds=rounds)
    print(scout_report(intel))
    with open(os.path.expanduser("~/.vigil/recon_log.jsonl"), "a") as f:
        f.write(json.dumps({"target": target, "rounds": rounds,
                            "summary": intel["summary"]}) + "\n")


if __name__ == "__main__":
    main()