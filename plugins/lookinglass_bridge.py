#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: core, datetime, os,, pathlib, plugins
# ROLE: lookinglass_bridge.py — Visual Cortex for JANUS
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
lookinglass_bridge.py — Visual Cortex for JANUS
Cursor position → Loom graph → Whorl 3D scene → Dashboard overlay.
"""

import os, sys, json, ast, math
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment
from plugins.loom_graph import LoomGraph
from plugins.whorl_translator import WhorlTranslator

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class LookinglassBridge:
    """
    Resolves code position to 3D component preview.
    
    Pipeline:
      cursor (file, line) → Loom query → Whorl subgraph → Three.js scene
    """
    
    def __init__(self, loom=None, whorl_translator=None):
        self.loom = loom or LoomGraph()
        self.whorl = whorl_translator or WhorlTranslator()
        self.codebase_root = Path(_PROJECT_ROOT)
        
    def watch(self, file_path: str, line_number: int) -> dict:
        """
        Given a cursor position, find the enclosing function/class
        and return its Loom node ID.
        """
        full_path = self.codebase_root / file_path
        if not full_path.exists():
            return {"status": "error", "reason": f"File not found: {file_path}"}
        
        # Parse the file to find the symbol at that line
        try:
            tree = ast.parse(full_path.read_text())
        except:
            return {"status": "error", "reason": "Cannot parse file"}
        
        symbol_name = None
        for node in ast.walk(tree):
            if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                if node.lineno <= line_number <= node.end_lineno:
                    if isinstance(node, ast.FunctionDef):
                        symbol_name = node.name
                    elif isinstance(node, ast.ClassDef):
                        symbol_name = node.name
        
        if not symbol_name:
            # Try to find the nearest function/class above the cursor
            symbol_name = self._nearest_symbol(tree, line_number)
        
        if not symbol_name:
            return {"status": "no_symbol", "file": file_path, "line": line_number}
        
        # Build a node ID consistent with how Loom weaves files
        node_id = f"{file_path}::{symbol_name}"
        
        deposit_sediment("lookinglass", "WATCH", node_id, 
                        "resolved", {"file": file_path, "line": line_number, "symbol": symbol_name})
        
        return {
            "status": "resolved",
            "file": file_path,
            "line": line_number,
            "symbol": symbol_name,
            "node_id": node_id
        }
    
    def _nearest_symbol(self, tree, line_number):
        """Find the nearest function/class definition above the cursor line."""
        nearest = None
        nearest_line = 0
        for node in ast.walk(tree):
            if hasattr(node, 'lineno'):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if node.lineno <= line_number and node.lineno > nearest_line:
                        nearest = node.name
                        nearest_line = node.lineno
        return nearest
    
    def resolve(self, node_id: str, depth: int = 2) -> dict:
        """
        Query Loom for the component's dependency graph.
        Returns a subgraph of nodes and edges around the target node.
        """
        # Try to get fiber neighborhood from Loom
        try:
            neighborhood = self.loom.get_fiber_neighborhood(node_id, depth=depth)
        except Exception:
            neighborhood = None
        
        if not neighborhood or (isinstance(neighborhood, dict) and not neighborhood.get("neighbors")):
            # Fallback: create a minimal graph from file structure
            return self._fallback_graph(node_id)
        
        # Convert Loom subgraph to Whorl-compatible scene description
        scene = self._loom_to_scene(neighborhood, node_id)
        
        deposit_sediment("lookinglass", "RESOLVE", node_id,
                        "rendered", {"nodes": len(scene.get("objects", []))})
        
        return {
            "status": "resolved",
            "node_id": node_id,
            "scene": scene
        }
    
    def _loom_to_scene(self, neighborhood, center_node_id):
        """Convert a Loom neighborhood into a Three.js scene description."""
        scene = {
            "objects": [],
            "camera": {"position": [0, 0, 3], "lookAt": [0, 0, 0]},
            "lights": [
                {"type": "ambient", "color": "#222244", "intensity": 0.5},
                {"type": "point", "position": [2, 2, 2], "color": "#ffaa00", "intensity": 1.0}
            ]
        }
        
        nodes = []
        if hasattr(self.loom.G, 'nodes'):
            # NetworkX
            nodes = list(neighborhood.nodes(data=True)) if hasattr(neighborhood, 'nodes') else []
        else:
            # Fallback dict
            nodes = [(nid, neighborhood["nodes"].get(nid, {})) for nid in neighborhood.get("neighbors", [])]
            # Add center node
            center_data = neighborhood.get("node", {})
            nodes.append((center_node_id, center_data))
        
        # Position nodes in a circle around the center
        center_x, center_y, center_z = 0, 0, 0
        other_nodes = [(nid, data) for nid, data in nodes if nid != center_node_id]
        center_data = next((data for nid, data in nodes if nid == center_node_id), {})
        
        # Center node
        scene["objects"].append({
            "type": "sphere",
            "id": center_node_id,
            "name": center_node_id.split("::")[-1] if "::" in center_node_id else center_node_id,
            "position": [center_x, center_y, center_z],
            "radius": 0.15,
            "color": "#ffaa00",
            "opacity": 1.0,
            "is_center": True
        })
        
        # Orbiting dependencies
        for i, (nid, data) in enumerate(other_nodes):
            angle = (2 * math.pi * i) / max(len(other_nodes), 1)
            radius = 1.0
            x = center_x + radius * math.cos(angle)
            y = center_y + (i % 3 - 1) * 0.4
            z = center_z + radius * math.sin(angle)
            scene["objects"].append({
                "type": "sphere",
                "id": nid,
                "name": nid.split("::")[-1] if isinstance(nid, str) and "::" in nid else str(nid),
                "position": [x, y, z],
                "radius": 0.08,
                "color": "#4488ff",
                "opacity": 0.8,
                "orbits": center_node_id
            })
        
        # Add edges as thin cylinders (approximated as line-like objects)
        # For now, use tiny spheres along the path
        if hasattr(self.loom.G, 'edges'):
            edges = list(self.loom.G.edges(data=True))
            for u, v, data in edges:
                if u == center_node_id or v == center_node_id:
                    # Add a connecting line indicator
                    scene["objects"].append({
                        "type": "edge",
                        "from": u,
                        "to": v,
                        "color": "#ffffff22"
                    })
        
        return scene
    
    def _fallback_graph(self, node_id):
        """Create a minimal scene from code structure when Loom data is sparse."""
        parts = node_id.split("::")
        file_path = parts[0] if len(parts) > 0 else ""
        symbol = parts[1] if len(parts) > 1 else "unknown"
        
        scene = {
            "objects": [
                {
                    "type": "sphere",
                    "id": node_id,
                    "name": symbol,
                    "position": [0, 0, 0],
                    "radius": 0.12,
                    "color": "#00ff88",
                    "opacity": 0.9
                }
            ],
            "camera": {"position": [0, 0, 2], "lookAt": [0, 0, 0]},
            "lights": [
                {"type": "ambient", "color": "#111133", "intensity": 0.5}
            ]
        }
        return {"status": "fallback", "node_id": node_id, "scene": scene}
    
    def render(self, scene: dict, dashboard_socket=None):
        """
        Push the scene to the dashboard's Whorl 3D panel.
        If dashboard_socket is provided, emit via WebSocket.
        """
        if dashboard_socket:
            dashboard_socket.emit('lookinglass_scene', scene)
            return {"status": "rendered", "via": "websocket"}
        
        # Otherwise, just return the scene for direct use
        return {"status": "rendered", "scene": scene}
    
    def full_pipeline(self, file_path: str, line_number: int, depth: int = 2) -> dict:
        """Watch → Resolve → Render, complete pipeline."""
        watch_result = self.watch(file_path, line_number)
        if watch_result["status"] != "resolved":
            return watch_result
        
        resolve_result = self.resolve(watch_result["node_id"], depth)
        return resolve_result
