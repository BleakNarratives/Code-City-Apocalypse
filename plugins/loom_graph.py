#!/usr/bin/env python3
"""
loom_graph.py — The Loom: Data Fiber Topology Weaver
Layer 3.5 — The third axis. Turns JANUS into a dimensional knowledge graph.
NetworkX-powered, Cypher-inspired query interface, JaneBox-backed persistence.
"""

import os, sys, json, hashlib, time
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment
from plugins.janebox import JaneBox

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Optional: For visualization later
try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False
    print("⚠️ networkx not installed; falling back to internal graph. Install with: pip install networkx")

class LoomGraph:
    """
    Weaves a knowledge graph from JANUS events.
    Nodes: Whorls, Agents, Sessions, Rides, Tasks, Challenges.
    Edges: CREATED, PARTICIPATED, PASSED, FAILED, HANDED_OFF, etc.
    Queries use a simplified Cypher-like DSL.
    """

    def __init__(self, janebox=None):
        self.jb = janebox or JaneBox()
        self.graph_path = Path(os.path.join(_PROJECT_ROOT, "registry/loom"))
        self.graph_path.mkdir(parents=True, exist_ok=True)
        self.graph_file = self.graph_path / "loom_graph.json"

        if HAS_NX:
            self.G = nx.MultiDiGraph()
        else:
            self.G = self._empty_graph()

        self._load()

    def _empty_graph(self):
        return {"nodes": {}, "edges": []}

    def _load(self):
        if self.graph_file.exists():
            with open(self.graph_file) as f:
                data = json.load(f)
            if HAS_NX:
                self.G = nx.node_link_graph(data)
            else:
                self.G = data
        else:
            self._save()

    def _save(self):
        if HAS_NX:
            data = nx.node_link_data(self.G)
        else:
            data = self.G
        with open(self.graph_file, 'w') as f:
            json.dump(data, f, indent=2)

    def weave(self, subject_id, predicate, object_id, properties=None):
        """
        Weave a fiber: (subject)-[predicate]->(object)
        subject/object can be node IDs or dictionaries.
        """
        props = properties or {}
        props["timestamp"] = datetime.now(timezone.utc).isoformat()

        if isinstance(subject_id, dict):
            subj = subject_id
            subj_id = subj.get("id") or subj.get("whorl_key") or hashlib.sha256(str(subj).encode()).hexdigest()[:12]
            subj["id"] = subj_id
        else:
            subj_id = subject_id
            subj = {"id": subj_id}

        if isinstance(object_id, dict):
            obj = object_id
            obj_id = obj.get("id") or obj.get("whorl_key") or hashlib.sha256(str(obj).encode()).hexdigest()[:12]
            obj["id"] = obj_id
        else:
            obj_id = object_id
            obj = {"id": obj_id}

        if HAS_NX:
            self.G.add_node(subj_id, **subj)
            self.G.add_node(obj_id, **obj)
            self.G.add_edge(subj_id, obj_id, key=predicate, **props)
        else:
            self.G["nodes"][subj_id] = subj
            self.G["nodes"][obj_id] = obj
            self.G["edges"].append({
                "source": subj_id,
                "target": obj_id,
                "predicate": predicate,
                "properties": props
            })

        self._save()
        deposit_sediment("loom", "WEAVE", f"{subj_id}-{predicate}->{obj_id}", "woven", props)

    def query(self, pattern):
        """
        Execute a simple graph pattern. Example syntax:
        MATCH (a:Agent)-[r:CREATED]->(w:Whorl) RETURN a, r, w
        or keywords: find agents, find whorls by agent X, etc.
        """
        results = []
        if HAS_NX:
            if "MATCH" in pattern.upper():
                # Very basic MATCH parser
                parts = pattern.upper().replace("MATCH ", "").split(" RETURN ")
                match_clause = parts[0].strip()
                # Extract node/edge patterns
                # (a:Agent)-[r:CREATED]->(w:Whorl)
                import re
                node_edge = re.findall(r'\((\w+):?(\w*)\)-\[(\w+):?(\w*)\]->\((\w+):?(\w*)\)', match_clause)
                if node_edge:
                    src_var, src_label, edge_var, edge_label, tgt_var, tgt_label = node_edge[0]
                    for u, v, k, data in self.G.edges(keys=True, data=True):
                        if edge_label and k != edge_label:
                            continue
                        src_data = self.G.nodes[u]
                        tgt_data = self.G.nodes[v]
                        if src_label and src_data.get("type", "") != src_label:
                            continue
                        if tgt_label and tgt_data.get("type", "") != tgt_label:
                            continue
                        results.append({src_var: src_data, edge_var: {"predicate": k, **data}, tgt_var: tgt_data})
        else:
            # Fallback simple queries
            if "find agents" in pattern.lower():
                results = [{"agent": node} for nid, node in self.G["nodes"].items() if node.get("type") == "Agent"]
            elif "find whorls" in pattern.lower():
                results = [{"whorl": node} for nid, node in self.G["nodes"].items() if node.get("type") == "Whorl"]
            elif "find edges" in pattern.lower():
                results = self.G["edges"]
        return results

    def get_fiber_neighborhood(self, node_id, depth=1):
        """Get the connected subgraph around a node."""
        if HAS_NX:
            sub = nx.ego_graph(self.G, node_id, radius=depth)
            return nx.node_link_data(sub)
        else:
            # Simple BFS
            visited = set()
            neighbors = []
            queue = [(node_id, 0)]
            while queue:
                nid, d = queue.pop(0)
                if nid in visited or d > depth:
                    continue
                visited.add(nid)
                for edge in self.G["edges"]:
                    if edge["source"] == nid and edge["target"] not in visited:
                        neighbors.append(edge["target"])
                        queue.append((edge["target"], d+1))
                    elif edge["target"] == nid and edge["source"] not in visited:
                        neighbors.append(edge["source"])
                        queue.append((edge["source"], d+1))
            return {"node": self.G["nodes"].get(node_id), "neighbors": [self.G["nodes"].get(n) for n in neighbors]}

    def weave_from_sediment(self, sediment_entries):
        """Auto-weave graph from deposit_sediment events."""
        for entry in sediment_entries:
            agent = entry.get("agent_id", "unknown")
            action = entry.get("action", "UNKNOWN")
            target = entry.get("target", "")
            self.weave(
                {"id": agent, "type": "Agent"},
                action,
                {"id": target, "type": "Target"},
                entry.get("metadata", {})
            )

# Quick seed function to weave existing JANUS state
def seed_loom():
    loom = LoomGraph()
    jb = JaneBox()
    # Weave existing sessions, challenges, rides
    sessions_dir = Path(os.path.join(_PROJECT_ROOT, "registry/sessions"))
    if sessions_dir.exists():
        for sf in sessions_dir.glob("*.json"):
            with open(sf) as f:
                sess = json.load(f)
            loom.weave(
                {"id": sess["agent_id"], "type": "Agent"},
                "HAS_SESSION",
                {"id": sess["session_id"], "type": "Session", "data": sess},
                {"created": sess["created_at"]}
            )
    print("✅ Loom seeded from sessions")
    return loom
