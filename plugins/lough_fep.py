#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: collections, core, datetime, os,
# ROLE: LOUGH/FEP — Legacy Overlay Unified Graphics Hub + Field Excited Programming
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
LOUGH/FEP — Legacy Overlay Unified Graphics Hub + Field Excited Programming

Phase 3 of JANUS. Pure Python graphics engine. No external deps beyond stdlib.
- Force-directed Whorl→SVG rendering (Fruchterman-Reingold)
- GeoWhorl: Web Mercator projection onto Google Maps tiles
- Camelot Wheel: harmonic mixing overlay (circle of fifths for code)
- FEP Runtime: decayed BFS signal propagation with trap capability gating
- CEP: attention cascade, drift detection via Jaccard similarity, emergence scoring

Part of ShipWrekD OS.
"""

import os, sys, math, json, hashlib
from datetime import datetime, timezone
from collections import deque

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _PROJECT_ROOT)

from core.JANUS import deposit_sediment


# ═══════════════════════════════════════════════════════════════════
# CAMELOT WHEEL — DJ harmonic mixing system applied to Whorl agents
# ═══════════════════════════════════════════════════════════════════

# The Camelot wheel has 24 positions: 1B–12B (outer/major ring) and
# 1A–12A (inner/minor ring). Each position maps to a musical key.
# Adjacent positions are harmonically compatible. We map Whorl agent
# hashes to these positions and use adjacency for agent compatibility.

CAMELOT_KEYS = {
    # B ring (Major, outer)
    "1B":  "C major",
    "2B":  "G major",
    "3B":  "D major",
    "4B":  "A major",
    "5B":  "E major",
    "6B":  "B major",
    "7B":  "F# major",
    "8B":  "Db major",
    "9B":  "Ab major",
    "10B": "Eb major",
    "11B": "Bb major",
    "12B": "F major",
    # A ring (Minor, inner)
    "1A":  "A minor",
    "2A":  "E minor",
    "3A":  "B minor",
    "4A":  "F# minor",
    "5A":  "C# minor",
    "6A":  "G# minor",
    "7A":  "Eb minor",
    "8A":  "Bb minor",
    "9A":  "F minor",
    "10A": "C minor",
    "11A": "G minor",
    "12A": "D minor",
}


def camelot_position(whorl_hash: str) -> tuple:
    """
    Map a whorl hash to a Camelot wheel position.
    Returns (ring, hour, key_name) where ring=0 is A/Minor, ring=1 is B/Major.
    """
    h = int(hashlib.sha256(whorl_hash.encode()).hexdigest()[:8], 16)
    ring = h % 2                          # 0 = A/minor, 1 = B/major
    hour = (h % 12) + 1                   # 1–12
    key_name = f"{hour}{'B' if ring else 'A'}"
    human_key = CAMELOT_KEYS.get(key_name, "unknown")
    return (ring, hour, key_name, human_key)


def camelot_is_compatible(pos1: tuple, pos2: tuple) -> bool:
    """
    Check if two Camelot positions are harmonically compatible.
    Compatible if:
      - Same hour, different ring (relative minor/major) OR
      - Adjacent hours (diff 1 or 11), same ring
    """
    ring1, hour1, _, _ = pos1
    ring2, hour2, _, _ = pos2

    if hour1 == hour2 and ring1 != ring2:
        return True  # Relative minor/major

    hour_diff = abs(hour1 - hour2)
    if hour_diff in (1, 11) and ring1 == ring2:
        return True  # Adjacent on same ring

    return False


# ═══════════════════════════════════════════════════════════════════
# WEB MERCATOR PROJECTION — lat/lng → pixel coordinates
# ═══════════════════════════════════════════════════════════════════

def latlng_to_world(lat: float, lng: float) -> tuple:
    """
    Convert lat/lng to Web Mercator world coordinates (0–256).
    Google Maps uses this projection for static map tiles.
    """
    x = 256.0 * (lng + 180.0) / 360.0
    lat_rad = math.radians(lat)
    y = 128.0 * (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi)
    return (x, y)


def world_to_pixel(wx: float, wy: float, zoom: int) -> tuple:
    """Convert world coordinates to pixel coordinates at given zoom level."""
    scale = 2 ** zoom
    return (wx * scale, wy * scale)


def latlng_to_pixel(lat: float, lng: float, zoom: int) -> tuple:
    """Direct lat/lng to pixel coordinates at zoom level."""
    wx, wy = latlng_to_world(lat, lng)
    return world_to_pixel(wx, wy, zoom)


# ═══════════════════════════════════════════════════════════════════
# LOUGH/FEP — Main Engine
# ═══════════════════════════════════════════════════════════════════

class LOUGH_FEP:
    """
    Legacy Overlay Unified Graphics Hub + Field Excited Programming Runtime.

    Integrates with JaneBox (shared state), LoomGraph (knowledge graph),
    and TrapRegistry (capability gates). All rendering is pure Python SVG —
    no external graphics libraries needed.
    """

    # ── Force-directed layout constants ──────────────────────────
    FD_ITERATIONS = 80          # Fruchterman-Reingold iterations
    FD_COOLING = 0.95           # Temperature decay per iteration
    FD_AREA_W = 800             # SVG viewport width
    FD_AREA_H = 600             # SVG viewport height
    FD_K_SCALE = 1.0            # Optimal distance scaling factor

    # ── FEP field constants ──────────────────────────────────────
    FEP_DECAY_LAMBDA = 0.5      # Signal decay per hop (e^-λ)
    FEP_MAX_HOPS = 10           # Max propagation depth

    # ── CEP constants ────────────────────────────────────────────
    CEP_HEAT_DECAY = 0.9        # Global heat decay per cycle
    CEP_DRIFT_THRESHOLD = 0.3   # Jaccard similarity below this = drifted

    def __init__(self, loom=None):
        """
        Bind to shared state.

        Args:
            loom:  LoomGraph instance for topology queries (optional).
        """
        self.loom = loom
        self._field_state = {}       # node_id → charge
        self._attention_heat = {}    # whorl_key → heat score
        self._trap_functions = {}    # capability_level → list of {trap_id, challenge_fn}

    # ═══════════════════════════════════════════════════════════
    # LOUGH: Graphics Hub
    # ═══════════════════════════════════════════════════════════

    def render_whorl_to_svg(self, whorl_graph: dict,
                            overlay_type: str = "spatial") -> str:
        """
        Convert Whorl graph to SVG using Fruchterman-Reingold
        force-directed layout. Nodes are colored by Camelot position.

        Args:
            whorl_graph:    Dict with 'nodes' and 'edges' keys.
                            Each node: {id, name, r, theta, z, entropy, ...}
                            Each edge: {source, target, weight}
            overlay_type:   'spatial' (2D force-directed) or 'camelot'
                            (pre-positioned on Camelot wheel).

        Returns:
            SVG string ready to write to .svg file or embed in HTML.
        """
        nodes = whorl_graph.get("nodes", [])
        edges = whorl_graph.get("edges", [])

        if not nodes:
            return self._empty_svg("No Whorl agents to render")

        if overlay_type == "camelot":
            return self._render_camelot_svg(nodes, edges)
        return self._render_force_directed_svg(nodes, edges)

    def _render_force_directed_svg(self, nodes: list, edges: list) -> str:
        """Fruchterman-Reingold force-directed layout → SVG."""
        n = len(nodes)
        area = self.FD_AREA_W * self.FD_AREA_H
        k = self.FD_K_SCALE * math.sqrt(area / n) if n > 1 else 100.0

        # ── Initialize positions randomly ────────────────────
        positions = {}
        for node in nodes:
            nid = node.get("id", node.get("name", "?"))
            # Use hashlib for deterministic positioning (hash() is randomized per process)
            seed_x = int(hashlib.sha256(f"{nid}_x".encode()).hexdigest()[:8], 16)
            seed_y = int(hashlib.sha256(f"{nid}_y".encode()).hexdigest()[:8], 16)
            positions[nid] = [
                self.FD_AREA_W * 0.5 + (seed_x % 200 - 100),
                self.FD_AREA_H * 0.5 + (seed_y % 200 - 100),
            ]

        # ── Build adjacency for fast lookup ──────────────────
        adjacency = {n.get("id", n.get("name", "?")): [] for n in nodes}
        for edge in edges:
            src = edge.get("source", edge.get("from", ""))
            tgt = edge.get("target", edge.get("to", ""))
            if src in adjacency:
                adjacency[src].append(tgt)
            if tgt in adjacency:
                adjacency[tgt].append(src)

        # ── Iterate ──────────────────────────────────────────
        temp = self.FD_AREA_W / 10.0
        for iteration in range(self.FD_ITERATIONS):
            # Calculate repulsive forces (all pairs)
            displacements = {nid: [0.0, 0.0] for nid in positions}

            node_ids = list(positions.keys())
            for i in range(len(node_ids)):
                for j in range(i + 1, len(node_ids)):
                    nid_i, nid_j = node_ids[i], node_ids[j]
                    dx = positions[nid_i][0] - positions[nid_j][0]
                    dy = positions[nid_i][1] - positions[nid_j][1]
                    dist = math.sqrt(dx * dx + dy * dy) + 0.01
                    force = k * k / dist
                    fx = force * dx / dist
                    fy = force * dy / dist
                    displacements[nid_i][0] += fx
                    displacements[nid_i][1] += fy
                    displacements[nid_j][0] -= fx
                    displacements[nid_j][1] -= fy

            # Calculate attractive forces (edges only)
            for edge in edges:
                src = edge.get("source", edge.get("from", ""))
                tgt = edge.get("target", edge.get("to", ""))
                if src in positions and tgt in positions:
                    dx = positions[src][0] - positions[tgt][0]
                    dy = positions[src][1] - positions[tgt][1]
                    dist = math.sqrt(dx * dx + dy * dy) + 0.01
                    force = dist * dist / k
                    fx = force * dx / dist
                    fy = force * dy / dist
                    displacements[src][0] -= fx
                    displacements[src][1] -= fy
                    displacements[tgt][0] += fx
                    displacements[tgt][1] += fy

            # Apply displacements with temperature cap
            for nid in positions:
                dx, dy = displacements[nid]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > 0:
                    capped = min(dist, temp)
                    positions[nid][0] += dx / dist * capped
                    positions[nid][1] += dy / dist * capped
                # Clamp to viewport
                positions[nid][0] = max(20, min(self.FD_AREA_W - 20,
                                                positions[nid][0]))
                positions[nid][1] = max(20, min(self.FD_AREA_H - 20,
                                                positions[nid][1]))

            temp *= self.FD_COOLING

        # ── Generate SVG ─────────────────────────────────────
        return self._positions_to_svg(positions, nodes, edges)

    def _positions_to_svg(self, positions: dict, nodes: list, edges: list) -> str:
        """Convert computed positions + node/edge data into SVG markup."""
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {self.FD_AREA_W} {self.FD_AREA_H}" '
            f'width="{self.FD_AREA_W}" height="{self.FD_AREA_H}">',
            f'<rect width="100%" height="100%" fill="#0a0e0a"/>',
            f'<style>',
            f'  .edge {{ stroke: #1a4a1a; stroke-width: 1; opacity: 0.6; }}',
            f'  .node {{ stroke: #0f380f; stroke-width: 2; }}',
            f'  .label {{ font-family: monospace; font-size: 10px; fill: #8bac0f; }}',
            f'</style>',
            f'<g id="edges">',
        ]

        # Edges
        for edge in edges:
            src = edge.get("source", edge.get("from", ""))
            tgt = edge.get("target", edge.get("to", ""))
            if src in positions and tgt in positions:
                lines.append(
                    f'<line class="edge" '
                    f'x1="{positions[src][0]:.1f}" y1="{positions[src][1]:.1f}" '
                    f'x2="{positions[tgt][0]:.1f}" y2="{positions[tgt][1]:.1f}"/>'
                )

        lines.append('</g><g id="nodes">')

        # Nodes — colored by Camelot position
        for node in nodes:
            nid = node.get("id", node.get("name", "?"))
            if nid not in positions:
                continue
            x, y = positions[nid]
            r = max(5, min(30, node.get("entropy", 50) * 0.3))
            cp = camelot_position(nid)
            # Color based on Camelot ring
            color = "#8bac0f" if cp[0] == 0 else "#306230"  # A=green, B=deep green
            if node.get("fossil"):
                color = "#444444"

            lines.append(
                f'<circle class="node" cx="{x:.1f}" cy="{y:.1f}" '
                f'r="{r:.1f}" fill="{color}" opacity="0.85"/>'
            )
            name = (node.get("name", nid)[:8])
            lines.append(
                f'<text class="label" x="{x:.1f}" y="{y + r + 12:.1f}" '
                f'text-anchor="middle">{name}</text>'
            )

        lines.append('</g></svg>')
        return "\n".join(lines)

    def _render_camelot_svg(self, nodes: list, edges: list) -> str:
        """
        Render nodes positioned on the Camelot wheel (two concentric rings).
        """
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="-220 -220 440 440" width="440" height="440">',
            f'<rect x="-220" y="-220" width="440" height="440" fill="#0a0e0a"/>',
            f'<style>',
            f'  .cam-edge {{ stroke:#1a4a1a; stroke-width:0.8; opacity:0.5; }}',
            f'  .cam-edge.compat {{ stroke:#8bac0f; stroke-width:2; opacity:0.8; }}',
            f'  .cam-label {{ font-family:monospace; font-size:8px; fill:#8bac0f; text-anchor:middle; }}',
            f'  .cam-key {{ font-family:monospace; font-size:6px; fill:#444; text-anchor:middle; }}',
            f'</style>',
        ]

        # Draw Camelot wheel background
        for hour in range(1, 13):
            for ring in (0, 1):
                r = 100 if ring == 0 else 150
                angle = math.pi / 2 - hour * math.pi / 6
                x = r * math.cos(angle)
                y = -r * math.sin(angle)
                key_name = f"{hour}{'A' if ring == 0 else 'B'}"
                # Tick mark
                tick_r = r + 15
                tx = tick_r * math.cos(angle)
                ty = -tick_r * math.sin(angle)
                lines.append(
                    f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{tx:.0f}" y2="{ty:.0f}" '
                    f'stroke="#306230" stroke-width="1"/>'
                )
                lines.append(
                    f'<text class="cam-key" x="{tx:.0f}" y="{ty:.0f}" '
                    f'dy="12">{key_name}</text>'
                )

        # Map nodes to Camelot positions
        node_positions = {}
        for node in nodes:
            nid = node.get("id", node.get("name", "?"))
            ring, hour, key_name, _ = camelot_position(nid)
            r = 65 if ring == 0 else 115
            angle = math.pi / 2 - hour * math.pi / 6
            # Use hashlib for deterministic jitter (hash() is randomized per process)
            jitter_x = (int(hashlib.sha256(f"{nid}x".encode()).hexdigest()[:4], 16) % 20 - 10)
            jitter_y = (int(hashlib.sha256(f"{nid}y".encode()).hexdigest()[:4], 16) % 20 - 10)
            x = r * math.cos(angle) + jitter_x
            y = -r * math.sin(angle) + jitter_y
            node_positions[nid] = (x, y, ring)

        # Edges
        for edge in edges:
            src = edge.get("source", edge.get("from", ""))
            tgt = edge.get("target", edge.get("to", ""))
            if src in node_positions and tgt in node_positions:
                compat = camelot_is_compatible(
                    camelot_position(src), camelot_position(tgt)
                )
                cls = "cam-edge compat" if compat else "cam-edge"
                lines.append(
                    f'<line class="{cls}" '
                    f'x1="{node_positions[src][0]:.0f}" y1="{node_positions[src][1]:.0f}" '
                    f'x2="{node_positions[tgt][0]:.0f}" y2="{node_positions[tgt][1]:.0f}"/>'
                )

        # Nodes
        for node in nodes:
            nid = node.get("id", node.get("name", "?"))
            if nid not in node_positions:
                continue
            x, y, ring = node_positions[nid]
            color = "#9bbc0f" if ring == 0 else "#306230"
            lines.append(
                f'<circle cx="{x:.0f}" cy="{y:.0f}" r="8" '
                f'fill="{color}" stroke="#0f380f" stroke-width="1.5" opacity="0.85"/>'
            )
            name = (node.get("name", nid)[:6])
            lines.append(
                f'<text class="cam-label" x="{x:.0f}" y="{y + 15:.0f}">{name}</text>'
            )

        lines.append('</svg>')
        return "\n".join(lines)

    def _empty_svg(self, message: str) -> str:
        """Return a minimal SVG with a message."""
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 400 100" width="400" height="100">'
            f'<rect width="100%" height="100%" fill="#0a0e0a"/>'
            f'<text x="200" y="55" text-anchor="middle" '
            f'font-family="monospace" font-size="14" fill="#8bac0f">'
            f'{message}</text></svg>'
        )

    def geo_overlay(self, whorl_graph: dict, lat: float, lng: float,
                    zoom: int = 14) -> str:
        """
        Generate a standalone SVG projection of Whorl nodes at their
        Web Mercator geo-positions, centered on (lat, lng). Includes
        reference grid and a tile-size frame where a real Google Maps
        static tile would be composited in a production renderer.

        Args:
            whorl_graph:  Dict with 'nodes'. Each node needs 'lat', 'lng' keys.
            lat, lng:     Center of the map.
            zoom:         Google Maps zoom level (0–21).
        """
        nodes = whorl_graph.get("nodes", [])
        if not nodes:
            return self._empty_svg("No geo-tagged Whorl agents")

        # ── Compute center pixel ────────────────────────────────
        cx, cy = latlng_to_pixel(lat, lng, zoom)

        # ── Compute per-node pixel offsets ───────────────────────
        geo_nodes = []
        for node in nodes:
            nlat = node.get("lat") or node.get("latitude")
            nlng = node.get("lng") or node.get("longitude")
            if nlat is None or nlng is None:
                continue
            px, py = latlng_to_pixel(nlat, nlng, zoom)
            # Offset from center
            dx, dy = px - cx, py - cy
            geo_nodes.append({
                "id": node.get("id", node.get("name", "?")),
                "name": node.get("name", node.get("id", "?")),
                "x": dx, "y": dy,
                "entropy": node.get("entropy", 50),
            })

        if not geo_nodes:
            return self._empty_svg("No nodes with lat/lng coordinates")

        # ── Build SVG with overlay ──────────────────────────────
        tile_size = 512
        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="-{tile_size//2} -{tile_size//2} {tile_size} {tile_size}" '
            f'width="{tile_size}" height="{tile_size}">',
            f'<rect x="-{tile_size//2}" y="-{tile_size//2}" '
            f'width="{tile_size}" height="{tile_size}" fill="#0a0e0a"/>',
            f'<!-- Map tile placeholder — Google Static Maps API tile goes here -->',
            f'<rect x="-{tile_size//2}" y="-{tile_size//2}" '
            f'width="{tile_size}" height="{tile_size}" '
            f'fill="none" stroke="#306230" stroke-width="2"/>',
            f'<text x="0" y="-{tile_size//2 + 20}" text-anchor="middle" '
            f'font-family="monospace" font-size="11" fill="#8bac0f">'
            f'GEO·WHORL {lat:.4f},{lng:.4f} z{zoom}</text>',
        ]

        # ── Grid lines for reference ─────────────────────────────
        for i in range(-tile_size//2, tile_size//2, 64):
            lines.append(
                f'<line x1="{i}" y1="-{tile_size//2}" x2="{i}" y2="{tile_size//2}" '
                f'stroke="#1a2a1a" stroke-width="0.5"/>'
            )
            lines.append(
                f'<line x1="-{tile_size//2}" y1="{i}" x2="{tile_size//2}" y2="{i}" '
                f'stroke="#1a2a1a" stroke-width="0.5"/>'
            )

        # ── Center crosshair ─────────────────────────────────────
        lines.append(
            f'<circle cx="0" cy="0" r="8" fill="none" stroke="#8bac0f" '
            f'stroke-width="2" stroke-dasharray="3,2"/>'
        )

        # ── Nodes ────────────────────────────────────────────────
        for gn in geo_nodes:
            r = max(4, min(20, gn["entropy"] * 0.25))
            color = "#8bac0f"
            lines.append(
                f'<circle cx="{gn["x"]:.0f}" cy="{gn["y"]:.0f}" r="{r:.0f}" '
                f'fill="{color}" stroke="#0f380f" stroke-width="1.5" opacity="0.85"/>'
            )
            lines.append(
                f'<text x="{gn["x"]:.0f}" y="{gn["y"] + r + 11:.0f}" '
                f'text-anchor="middle" font-family="monospace" font-size="8" '
                f'fill="#9bbc0f">{gn["name"][:8]}</text>'
            )

        lines.append('</svg>')
        return "\n".join(lines)

    def camelot_overlay(self, whorl_graph: dict,
                        key: str = "Cmin") -> str:
        """
        Map Whorl tension edges to Camelot wheel positions.
        Returns SVG with nodes positioned on the wheel and
        harmonic compatibility edges highlighted.

        Args:
            whorl_graph:  Dict with 'nodes' and 'edges'.
            key:          Reference key displayed in the SVG title.
        """
        svg = self.render_whorl_to_svg(whorl_graph, overlay_type="camelot")
        # Inject the reference key into the SVG title area
        svg = svg.replace(
            '<svg ',
            f'<!-- Camelot Wheel · Reference Key: {key} -->\n<svg ',
            1
        )
        return svg

    # ═══════════════════════════════════════════════════════════
    # FEP: Field Excited Programming Runtime
    # ═══════════════════════════════════════════════════════════

    def excite_field(self, signal_pattern: dict,
                     field_graph: dict) -> list:
        """
        Propagate a signal through the field graph using decayed BFS.
        Each hop reduces signal charge by e^-λ.

        Args:
            signal_pattern:  {node_id: initial_charge}
            field_graph:     {nodes: [{id, ...}], edges: [{source, target}]}

        Returns:
            List of {node_id, charge, hops, path} for each reached node.
        """
        if not signal_pattern or not field_graph:
            return []

        # Build adjacency
        adj = {}
        for node in field_graph.get("nodes", []):
            adj[node.get("id", node.get("name", "?"))] = []
        for edge in field_graph.get("edges", []):
            src = edge.get("source", edge.get("from", ""))
            tgt = edge.get("target", edge.get("to", ""))
            if src in adj:
                adj[src].append(tgt)
            if tgt in adj:
                adj[tgt].append(src)

        # BFS with decay
        visited = {}
        queue = deque()

        for node_id, charge in signal_pattern.items():
            if node_id in adj:
                queue.append((node_id, charge, 0, [node_id]))
                visited[node_id] = charge

        collapse_path = []

        while queue:
            node_id, charge, hops, path = queue.popleft()
            if hops > self.FEP_MAX_HOPS:
                continue

            collapse_path.append({
                "node_id": node_id,
                "charge": round(charge, 4),
                "hops": hops,
                "path": path,
            })

            next_charge = charge * math.exp(-self.FEP_DECAY_LAMBDA)
            if next_charge < 0.01:
                continue  # Signal too weak

            for neighbor in adj.get(node_id, []):
                if neighbor not in visited or visited[neighbor] < next_charge:
                    visited[neighbor] = next_charge
                    queue.append((neighbor, next_charge, hops + 1,
                                  path + [neighbor]))

        self._field_state = visited
        deposit_sediment("lough_fep", "EXCITE_FIELD", "field_graph",
                        f"propagated to {len(collapse_path)} nodes",
                        {"max_hops": max((c["hops"] for c in collapse_path),
                                        default=0)})
        return collapse_path

    def define_trap(self, capability_level: str, challenge_fn) -> str:
        """
        Register a trap function for capability gating in the FEP field.
        Multiple traps can be registered per capability level — all must
        be passed to gain access.

        Args:
            capability_level:  Required capability tier (e.g., 'scribe', 'architect').
            challenge_fn:      Callable that takes (agent_id, query) and returns bool.

        Returns:
            trap_id string.
        """
        if capability_level not in self._trap_functions:
            self._trap_functions[capability_level] = []
        
        trap_id = f"fep_trap_{capability_level}_{len(self._trap_functions[capability_level])}"
        self._trap_functions[capability_level].append({
            "trap_id": trap_id,
            "challenge_fn": challenge_fn,
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        deposit_sediment("lough_fep", "DEFINE_TRAP", capability_level,
                        "registered", {"trap_id": trap_id})
        return trap_id

    def query_with_trap(self, query: str, claimed_capability: str,
                        agent_id: str = "unknown") -> dict:
        """
        Query the FEP field. If a trap is set for the claimed capability,
        the agent must pass the challenge to access the field state.

        Args:
            query:              What the agent wants from the field.
            claimed_capability: The capability the agent claims to have.
            agent_id:           The agent making the query.

        Returns:
            {status, field_state, trap_passed, ...}
        """
        # Check if a trap exists for this capability level
        # _trap_functions maps capability_level → list of {trap_id, challenge_fn}
        traps = self._trap_functions.get(claimed_capability, [])

        if traps:
            # Attempt all traps for this capability level (must pass ALL)
            for trap in traps:
                try:
                    passed = trap["challenge_fn"](agent_id, query)
                except Exception:
                    passed = False

                if not passed:
                    deposit_sediment("lough_fep", "TRAP_BLOCKED", agent_id,
                                   "blocked", {"capability": claimed_capability})
                    return {
                        "status": "blocked",
                        "trap_id": trap["trap_id"],
                        "reason": f"Failed {claimed_capability} capability check",
                        "field_state": {},
                    }

            # All traps passed
            return {
                "status": "granted",
                "trap_passed": True,
                "capability": claimed_capability,
                "field_state": self._field_state,
                "query": query,
            }
        else:
            # No traps set — grant access freely
            deposit_sediment("lough_fep", "QUERY_FIELD", agent_id,
                            "granted", {"capability": claimed_capability})
            return {
                "status": "granted",
                "trap_passed": False,
                "capability": claimed_capability,
                "field_state": self._field_state,
                "query": query,
            }

    # ═══════════════════════════════════════════════════════════
    # CEP: Collective Emergence Protocol
    # ═══════════════════════════════════════════════════════════

    def attention_cascade(self, whorl_key: str,
                          agent_id: str) -> float:
        """
        Mark a whorl as "touched" by an agent. Increment its heat score.
        Heat decays globally over time (exponential decay).

        Returns the new heat score for this whorl.
        """
        # Global decay
        for wk in list(self._attention_heat.keys()):
            self._attention_heat[wk] *= self.CEP_HEAT_DECAY
            if self._attention_heat[wk] < 0.001:
                del self._attention_heat[wk]

        # Increment touched whorl
        if whorl_key not in self._attention_heat:
            self._attention_heat[whorl_key] = 1.0
        else:
            self._attention_heat[whorl_key] += 1.0

        deposit_sediment("lough_fep", "ATTENTION_CASCADE", whorl_key,
                        f"heat={self._attention_heat[whorl_key]:.2f}",
                        {"agent": agent_id})
        return self._attention_heat[whorl_key]

    def get_attention_heatmap(self) -> dict:
        """Return current attention heat scores across all whorls."""
        return dict(sorted(self._attention_heat.items(),
                          key=lambda x: x[1], reverse=True))

    def detect_drift(self, agent_output: str,
                     sediment_history: list,
                     ngram_size: int = 3) -> dict:
        """
        Flag outputs that diverge from sediment pattern using
        Jaccard similarity on character n-grams.

        Args:
            agent_output:      The agent's current output string.
            sediment_history:  List of sediment records (each with 'action', 'outcome').
            ngram_size:        Size of character n-grams for comparison.

        Returns:
            {drifted: bool, similarity: float, threshold: float}
        """
        if not sediment_history or not agent_output:
            return {"drifted": False, "similarity": 1.0,
                    "threshold": self.CEP_DRIFT_THRESHOLD}

        # Build sediment reference text from recent history
        sediment_text = " ".join(
            f"{r.get('action', '')} {r.get('outcome', '')}"
            for r in sediment_history[-10:]
        ).lower()

        # Character n-gram sets
        def ngrams(text: str, n: int) -> set:
            return {text[i:i+n] for i in range(len(text) - n + 1)}

        output_ngrams = ngrams(agent_output.lower(), ngram_size)
        sediment_ngrams = ngrams(sediment_text, ngram_size)

        if not output_ngrams or not sediment_ngrams:
            return {"drifted": False, "similarity": 1.0,
                    "threshold": self.CEP_DRIFT_THRESHOLD}

        intersection = output_ngrams & sediment_ngrams
        union = output_ngrams | sediment_ngrams
        similarity = len(intersection) / len(union) if union else 1.0

        drifted = similarity < self.CEP_DRIFT_THRESHOLD

        if drifted:
            deposit_sediment("lough_fep", "DRIFT_DETECTED", "agent_output",
                           "drifted", {"similarity": round(similarity, 4)})

        return {
            "drifted": drifted,
            "similarity": round(similarity, 4),
            "threshold": self.CEP_DRIFT_THRESHOLD,
        }

    def emergence_score(self, swarm_outputs: list,
                        individual_baselines: dict) -> dict:
        """
        Quantify swarm vs individual performance delta.
        Emergence > 1.0 means the swarm outperforms any individual.

        Args:
            swarm_outputs:       List of {agent_id, score} from swarm run.
            individual_baselines: {agent_id: baseline_score} from solo runs.

        Returns:
            {emergence_ratio, swarm_avg, best_individual, emerged: bool}
        """
        if not swarm_outputs or not individual_baselines:
            return {"emergence_ratio": 1.0, "emerged": False,
                    "swarm_avg": 0.0, "best_individual": 0.0}

        swarm_scores = [s.get("score", s.get("final_score", 0))
                       for s in swarm_outputs]
        swarm_avg = sum(swarm_scores) / len(swarm_scores) if swarm_scores else 0

        best_individual = max(individual_baselines.values()) if individual_baselines else 0
        emergence = swarm_avg / best_individual if best_individual > 0 else 1.0

        emerged = emergence > 1.0

        deposit_sediment("lough_fep", "EMERGENCE_SCORE", "swarm",
                        f"ratio={emergence:.3f}",
                        {"emerged": emerged, "ratio": round(emergence, 4)})

        return {
            "emergence_ratio": round(emergence, 4),
            "emerged": emerged,
            "swarm_avg": round(swarm_avg, 4),
            "best_individual": round(best_individual, 4),
        }
