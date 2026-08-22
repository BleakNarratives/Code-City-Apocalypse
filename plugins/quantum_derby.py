#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-general
# DEPS: core, datetime, os,, pathlib, plugins
# ROLE: Quantum Derby — Phase 2: PEQ Scoring, Observer Collapse, Wagers, Contest Layers,
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Module (3)
# [/DNA_TAG]

"""
Quantum Derby — Phase 2: PEQ Scoring, Observer Collapse, Wagers, Contest Layers,
                 Bayesian Odds Oracle, and vi/vx Experience Projections.

Part of ShipWrekD OS / JANUS. All persistence via JaneBox (Supabase).
No external ML libraries needed — pure Python math.
"""

import os, sys, json, hashlib, time, math, random
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment
from plugins.janebox import JaneBox
from plugins.derby import Derby

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ═══════════════════════════════════════════════════════════════════
# FREE ENTROPY SOURCES  —  Observer seed ingredients
# ═══════════════════════════════════════════════════════════════════

def fetch_moon_illumination() -> float:
    """Moon illumination fraction (0.0–1.0). Free API, no key needed."""
    try:
        import urllib.request
        ts = int(time.time())
        url = f"https://api.farmsense.net/v1/moonphases/?d={ts}"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read())
            return float(data[0]["Illumination"]) / 100.0
    except:
        return random.random()

def fetch_blockchain_height() -> int:
    """Bitcoin blockchain height as an integer entropy source."""
    try:
        import urllib.request
        with urllib.request.urlopen("https://blockchain.info/q/getblockcount", timeout=5) as resp:
            return int(resp.read().strip())
    except:
        return int(time.time()) % 100000

def fetch_atmospheric_noise() -> float:
    """Random.org atmospheric noise (0.0–1.0). Free tier."""
    try:
        import urllib.request
        url = "https://www.random.org/integers/?num=1&min=0&max=255&col=1&base=10&format=plain&rnd=new"
        with urllib.request.urlopen(url, timeout=5) as resp:
            return int(resp.read().strip()) / 255.0
    except:
        return random.random()


# ═══════════════════════════════════════════════════════════════════
# FREQUENCY DECAY PEQ PROFILES  —  EMA-based predictive accuracy
# ═══════════════════════════════════════════════════════════════════

class PEQProfiles:
    """
    Tracks per-agent Predictive Efficiency Quotient using exponential
    moving average (EMA) with configurable decay alpha.
    
    Lower alpha = slower decay (more weight on history).
    Higher alpha = faster decay (more weight on recent results).
    """
    
    DEFAULT_ALPHA = 0.2  # 20% weight on new result, 80% on history
    
    def __init__(self, janebox: JaneBox):
        self.jb = janebox
        self.peq_key = "quantum_peq_profiles"
        self._init_store()
    
    def _init_store(self):
        if not self.jb.read(self.peq_key):
            self.jb.write(self.peq_key, {"profiles": {}}, "peq_profiles", "system")
    
    def _get_profiles(self) -> dict:
        data = self.jb.read(self.peq_key)
        return data["payload"] if data else {"profiles": {}}
    
    def _save_profiles(self, profiles: dict):
        self.jb.write(self.peq_key, profiles, "peq_profiles", "system")
    
    def get_peq(self, agent_id: str) -> float:
        """Get current PEQ for an agent. Defaults to 0.5 (neutral prior)."""
        profiles = self._get_profiles()
        return profiles["profiles"].get(agent_id, {}).get("peq", 0.5)
    
    def update_peq(self, agent_id: str, accuracy: float, alpha: float = None):
        """
        Update PEQ using EMA: PEQ_new = alpha * accuracy + (1-alpha) * PEQ_old.
        
        Args:
            agent_id:  The agent being scored.
            accuracy:  0.0–1.0 — how well they performed this round.
            alpha:     Decay factor. None = use agent's stored alpha or DEFAULT.
        """
        profiles = self._get_profiles()
        agent_profile = profiles["profiles"].get(agent_id, {
            "peq": 0.5,
            "alpha": self.DEFAULT_ALPHA,
            "wins": 0,
            "losses": 0,
            "history": []
        })
        
        if alpha is None:
            alpha = agent_profile.get("alpha", self.DEFAULT_ALPHA)
        
        old_peq = agent_profile["peq"]
        new_peq = alpha * accuracy + (1 - alpha) * old_peq
        
        # Track win/loss for Bayesian prior
        if accuracy >= 0.6:
            agent_profile["wins"] += 1
        else:
            agent_profile["losses"] += 1
        
        # Rolling history (last 20 rounds for trajectory analysis)
        agent_profile["history"].append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "accuracy": accuracy,
            "peq": round(new_peq, 4)
        })
        if len(agent_profile["history"]) > 20:
            agent_profile["history"] = agent_profile["history"][-20:]
        
        agent_profile["peq"] = round(new_peq, 4)
        profiles["profiles"][agent_id] = agent_profile
        self._save_profiles(profiles)
        
        deposit_sediment("peq_profiles", "UPDATE_PEQ", agent_id,
                        f"PEQ {old_peq:.3f}→{new_peq:.3f}",
                        {"accuracy": accuracy, "alpha": alpha})
    
    def get_trajectory(self, agent_id: str) -> dict:
        """
        Calculate PEQ trajectory — slope of last N readings.
        Positive slope = improving. Negative = declining.
        """
        profiles = self._get_profiles()
        profile = profiles["profiles"].get(agent_id, {})
        history = profile.get("history", [])
        
        if len(history) < 2:
            return {"slope": 0.0, "trend": "flat", "readings": len(history)}
        
        # Linear regression on last 10 points
        points = history[-10:]
        n = len(points)
        x_mean = (n - 1) / 2.0
        y_values = [p["peq"] for p in points]
        y_mean = sum(y_values) / n
        
        numerator = sum((i - x_mean) * (y_values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator > 0 else 0.0
        
        trend = "rising" if slope > 0.01 else ("falling" if slope < -0.01 else "flat")
        return {"slope": round(slope, 4), "trend": trend, "readings": n}
    
    def get_win_loss(self, agent_id: str) -> tuple:
        """Return (wins, losses) for Bayesian prior."""
        profiles = self._get_profiles()
        profile = profiles["profiles"].get(agent_id, {})
        return (profile.get("wins", 0), profile.get("losses", 0))
    
    def list_agents(self) -> list:
        """
        Public API: return all tracked agent profiles as a list of dicts.
        Each dict has: agent_id, peq, wins, losses, history count.
        """
        profiles = self._get_profiles()
        result = []
        for agent_id, profile in profiles.get("profiles", {}).items():
            result.append({
                "agent_id": agent_id,
                "peq": profile.get("peq", 0.5),
                "wins": profile.get("wins", 0),
                "losses": profile.get("losses", 0),
                "alpha": profile.get("alpha", self.DEFAULT_ALPHA),
                "history_count": len(profile.get("history", [])),
            })
        result.sort(key=lambda x: x["peq"], reverse=True)
        return result


# ═══════════════════════════════════════════════════════════════════
# QUANTUM DERBY  —  Phase 2: Full contest engine
# ═══════════════════════════════════════════════════════════════════

class QuantumDerby:
    """
    Quantum Derby contest engine — Phase 2 complete.
    
    Contest layers:
      - 'private'   — Invite-only. Must be in access_list.
      - 'regional'  — Same-tier agents. Auto-promotes to global at threshold.
      - 'global'    — Open to all. No access restrictions.
      - 'festival'  — Tournament bracket mode. Max entries enforced.
    
    Scoring:  FrequencyDecay PEQ (EMA) + ObserverCollapse (deterministic).
    Odds:     Bayesian Beta-distribution with 95% credible intervals.
    Projections: vi (viewer engagement) + vx (agent trajectory).
    """
    
    # ── Constants ──────────────────────────────────────────────
    
    WAGER_TYPES = [
        "reputation",       # Stake reputation points
        "priority",         # Stake queue priority
        "trap_skip",        # Stake a trap-skip token
        "ride_sponsorship", # Sponsor an amusement park ride
        "vanity_wave",      # Dashboard takeover rights
    ]
    
    LAYERS = ["private", "regional", "global", "festival"]
    
    # Regional→Global promotion: auto-promote when submissions >= threshold
    REGIONAL_PROMOTION_THRESHOLD = 5
    
    # Festival bracket cap
    FESTIVAL_MAX_ENTRIES = 8
    
    # ── Lifecycle ──────────────────────────────────────────────
    
    def __init__(self, janebox: JaneBox = None, derby: Derby = None):
        self.jb = janebox or JaneBox()
        self.derby = derby or Derby(self.jb)
        self.peq = PEQProfiles(self.jb)
        self.contests_key = "quantum_derby_contests"
        self._init_contests()
    
    def _init_contests(self):
        if not self.jb.read(self.contests_key):
            self.jb.write(self.contests_key,
                         {"active_contests": [], "closed_contests": []},
                         "quantum_derby", "system")
    
    def _get_contests(self) -> dict:
        data = self.jb.read(self.contests_key)
        return data["payload"] if data else {"active_contests": [], "closed_contests": []}
    
    def _save_contests(self, contests: dict):
        self.jb.write(self.contests_key, contests, "quantum_derby", "system")
    
    # ── Contest Creation ───────────────────────────────────────
    
    def create_contest(self, task_id: str, layer: str = "regional",
                       duration_minutes: int = 10, creator: str = "system",
                       access_list: list = None, promotion_threshold: int = None,
                       max_entries: int = None) -> dict:
        """
        Create a new quantum contest.
        
        Args:
            task_id:            Derby task to compete on.
            layer:              'private' | 'regional' | 'global' | 'festival'
            duration_minutes:   How long the contest stays open.
            creator:            Who created it.
            access_list:        Agent IDs allowed (private layer only).
            promotion_threshold: Submissions needed for regional→global promotion.
            max_entries:        Max entries (festival layer only).
        """
        if layer not in self.LAYERS:
            return {"status": "rejected",
                    "reason": f"Unknown layer '{layer}'. Valid: {self.LAYERS}"}
        
        contests = self._get_contests()
        contest_id = hashlib.sha256(
            f"{task_id}{time.time()}".encode()
        ).hexdigest()[:12]
        
        contest = {
            "contest_id": contest_id,
            "task_id": task_id,
            "layer": layer,
            "creator": creator,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "closes_at": (datetime.now(timezone.utc) +
                         timedelta(minutes=duration_minutes)).isoformat(),
            "submissions": [],
            "wagers": [],
            "observer_seed": None,
            "collapsed": False,
            "final_scores": [],
            # ── Phase 2: Layer enforcement ──
            "access_list": access_list or [],
            "promotion_threshold": promotion_threshold or self.REGIONAL_PROMOTION_THRESHOLD,
            "max_entries": max_entries or self.FESTIVAL_MAX_ENTRIES,
            # ── Phase 2: vi/vx ──
            "entropy_vi": 0.0,      # Viewer engagement entropy
            "vi_history": [],        # Track VI over contest lifetime
        }
        
        contests["active_contests"].append(contest)
        self._save_contests(contests)
        deposit_sediment("quantum_derby", "CREATE_CONTEST", contest_id,
                        "active", {"layer": layer, "task": task_id})
        return contest
    
    # ── Entry Submission with Layer Enforcement ─────────────────
    
    def submit_entry(self, contest_id: str, agent_id: str, session_id: str,
                     solution_code: str, token_count: int,
                     projected_score: float = None) -> dict:
        """
        Submit a solution to an active contest.
        Enforces contest layer access rules.
        Also produces a vx (agent experience) projection.
        """
        contests = self._get_contests()
        contest = next((c for c in contests["active_contests"]
                       if c["contest_id"] == contest_id), None)
        if not contest:
            return {"status": "rejected", "reason": "Contest not found or closed"}
        
        # ── Layer access enforcement ───────────────────────────
        layer = contest.get("layer", "global")
        
        if layer == "private":
            access_list = contest.get("access_list", [])
            # Creator is always allowed; others must be on the access list
            if agent_id not in access_list and agent_id != contest.get("creator", ""):
                return {"status": "rejected",
                        "reason": f"Private contest — {agent_id} not in access list"}
        
        elif layer == "festival":
            if len(contest["submissions"]) >= contest.get("max_entries",
                                                          self.FESTIVAL_MAX_ENTRIES):
                return {"status": "rejected",
                        "reason": "Festival bracket full"}
        
        # regional and global have no entry restrictions
        
        # ── Create entry ───────────────────────────────────────
        entry = {
            "entry_id": hashlib.sha256(
                f"{contest_id}{agent_id}{time.time()}".encode()
            ).hexdigest()[:12],
            "agent_id": agent_id,
            "session_id": session_id,
            "solution_code": solution_code,
            "token_count": token_count,
            "projected_score": (projected_score or
                               self._project_score(agent_id, token_count)),
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            # ── Phase 2: vx projection ──
            "vx_trajectory": self._compute_vx(agent_id),
        }
        
        contest["submissions"].append(entry)
        
        # ── Regional → Global auto-promotion ───────────────────
        if (layer == "regional" and
            len(contest["submissions"]) >= contest.get("promotion_threshold",
                                                        self.REGIONAL_PROMOTION_THRESHOLD)):
            contest["layer"] = "global"
            deposit_sediment("quantum_derby", "PROMOTE_CONTEST", contest_id,
                           "regional→global",
                           {"entries": len(contest["submissions"])})
        
        self._save_contests(contests)
        deposit_sediment(agent_id, "QUANTUM_SUBMIT", contest_id,
                        "submitted",
                        {"projected": entry["projected_score"],
                         "vx": entry["vx_trajectory"]})
        
        return {
            "status": "submitted",
            "entry_id": entry["entry_id"],
            "vx": entry["vx_trajectory"],
        }
    
    # ── Wager System ───────────────────────────────────────────
    
    def place_wager(self, contest_id: str, from_agent: str, to_agent: str,
                    wager_type: str, stake: int = 10) -> dict:
        """Place a wager on a contestant. Types: reputation, priority,
           trap_skip, ride_sponsorship, vanity_wave."""
        contests = self._get_contests()
        contest = next((c for c in contests["active_contests"]
                       if c["contest_id"] == contest_id), None)
        if not contest:
            return {"status": "rejected", "reason": "Contest not active"}
        if wager_type not in self.WAGER_TYPES:
            return {"status": "rejected",
                    "reason": f"Unknown wager type. Valid: {self.WAGER_TYPES}"}
        
        wager = {
            "from": from_agent,
            "to": to_agent,
            "type": wager_type,
            "stake": stake,
            "placed_at": datetime.now(timezone.utc).isoformat()
        }
        contest["wagers"].append(wager)
        self._save_contests(contests)
        return {"status": "placed", "wager": wager}
    
    # ── Observer Collapse v2 — Deterministic quantum collapse ──
    
    def collapse_contest(self, contest_id: str) -> dict:
        """
        Collapse the quantum superposition.
        
        Phase 2 improvements:
        - Deterministic per-agent multipliers (not random.random())
        - PEQ profiles updated with actual accuracy
        - VI (viewer engagement) computed and stored
        """
        contests = self._get_contests()
        contest = next((c for c in contests["active_contests"]
                       if c["contest_id"] == contest_id), None)
        if not contest:
            return {"status": "rejected", "reason": "Contest not active"}
        
        # ── Generate observer seed from free entropy sources ────
        moon = fetch_moon_illumination()
        btc_height = fetch_blockchain_height()
        noise = fetch_atmospheric_noise()
        combined = f"{moon}:{btc_height}:{noise}:{time.time()}"
        seed = hashlib.sha256(combined.encode()).hexdigest()
        contest["observer_seed"] = seed
        
        # ── Deterministic collapse per agent ───────────────────
        final_scores = []
        for sub in contest["submissions"]:
            base_score = sub["projected_score"]
            
            # Deterministic multiplier from seed + agent_id
            multiplier = self._deterministic_collapse(seed, sub["agent_id"])
            
            final = base_score * multiplier
            final_scores.append({
                "entry_id": sub["entry_id"],
                "agent_id": sub["agent_id"],
                "projected": base_score,
                "observer_multiplier": round(multiplier, 3),
                "final_score": round(final, 4),
            })
        
        final_scores.sort(key=lambda x: x["final_score"], reverse=True)
        for i, s in enumerate(final_scores):
            s["rank"] = i + 1
        
        # ── Update PEQ profiles ────────────────────────────────
        if final_scores:
            top_score = final_scores[0]["final_score"]
            for s in final_scores:
                # Accuracy = how close to the winner
                accuracy = s["final_score"] / top_score if top_score > 0 else 0.5
                self.peq.update_peq(s["agent_id"], accuracy)
        
        # ── Compute VI (viewer engagement entropy) ─────────────
        vi = self._compute_vi(final_scores)
        contest["entropy_vi"] = vi
        contest["vi_history"].append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "vi": vi,
            "entrants": len(final_scores),
        })
        
        # ── Close contest ──────────────────────────────────────
        contest["final_scores"] = final_scores
        contest["collapsed"] = True
        contests["active_contests"] = [
            c for c in contests["active_contests"]
            if c["contest_id"] != contest_id
        ]
        contests["closed_contests"].append(contest)
        self._save_contests(contests)
        
        winner = final_scores[0]["agent_id"] if final_scores else "none"
        deposit_sediment("observer", "COLLAPSE", contest_id, "collapsed",
                        {"winner": winner, "vi": vi,
                         "entrants": len(final_scores)})
        
        return {
            "status": "collapsed",
            "final_scores": final_scores,
            "vi": vi,
            "observer_seed": seed[:12],
        }
    
    def _deterministic_collapse(self, observer_seed: str, agent_id: str) -> float:
        """
        Deterministic pseudo-random multiplier for observer collapse.
        
        Uses SHA-256(seed + agent_id) to produce a reproducible 0.8–1.2
        multiplier. Same seed + same agent = same result every time.
        """
        agent_hash = hashlib.sha256(
            f"{observer_seed}{agent_id}".encode()
        ).hexdigest()
        # Take first 8 hex chars as a 32-bit integer
        int_val = int(agent_hash[:8], 16)
        # Map to 0.8–1.2 range
        return 0.8 + (int_val / 0xFFFFFFFF) * 0.4
    
    # ── PEQ-based score projection ─────────────────────────────
    
    def _project_score(self, agent_id: str, token_count: int) -> float:
        """
        Project a score using PEQ profile + derby history + token efficiency.
        Phase 2: Uses FrequencyDecay PEQ as the primary signal.
        """
        peq_score = self.peq.get_peq(agent_id)
        
        # Blend with derby leaderboard if available
        lb = self.derby.get_leaderboard()
        agent_stats = next(
            (r for r in lb["rankings"] if r["agent_id"] == agent_id), None
        )
        if agent_stats:
            derby_avg = agent_stats["average"]
            # 60% PEQ, 40% derby history
            base = peq_score * 0.6 + derby_avg * 0.4
        else:
            base = peq_score
        
        efficiency = max(0, 1.0 - token_count / 4000)
        return round(base * 0.7 + efficiency * 0.3, 3)
    
    # ── Bayesian Odds Oracle ───────────────────────────────────
    
    def calculate_odds(self, contest_id: str) -> list:
        """
        Bayesian odds with Beta-distribution confidence intervals.
        
        Prior: Beta(1, 1) — uninformative uniform prior.
        Posterior: Beta(1 + wins, 1 + losses) per agent.
        
        Returns per-agent:
        - win_probability (mean of posterior)
        - ci_lower / ci_upper (95% credible interval via Normal approx)
        """
        contests = self._get_contests()
        contest = next(
            (c for c in contests["active_contests"] + contests["closed_contests"]
             if c["contest_id"] == contest_id), None
        )
        if not contest or not contest["submissions"]:
            return []
        
        submissions = contest["submissions"]
        odds = []
        
        for s in submissions:
            wins, losses = self.peq.get_win_loss(s["agent_id"])
            
            # Beta posterior parameters: prior Beta(1,1) → posterior Beta(1+wins, 1+losses)
            alpha_post = 1 + wins
            beta_post = 1 + losses
            
            # Mean of Beta distribution = win probability
            mu = alpha_post / (alpha_post + beta_post)
            
            # Blended probability: 70% Bayesian posterior, 30% projected score
            total_proj = sum(x["projected_score"] for x in submissions)
            proj_prob = (s["projected_score"] / total_proj
                        if total_proj > 0 else 1.0 / len(submissions))
            blended_prob = mu * 0.7 + proj_prob * 0.3
            
            # 95% credible interval via Normal approximation of Beta
            variance = (alpha_post * beta_post) / (
                (alpha_post + beta_post) ** 2 * (alpha_post + beta_post + 1)
            )
            std_dev = math.sqrt(variance) if variance > 0 else 0.0
            ci_half_width = 1.96 * std_dev
            
            odds.append({
                "agent_id": s["agent_id"],
                "projected": s["projected_score"],
                "win_probability": round(blended_prob, 4),
                "bayesian_mean": round(mu, 4),
                "ci_lower": round(max(0.0, blended_prob - ci_half_width), 4),
                "ci_upper": round(min(1.0, blended_prob + ci_half_width), 4),
                "confidence": "95%",
                "wins": wins,
                "losses": losses,
                "vx": s.get("vx_trajectory", {}),
            })
        
        odds.sort(key=lambda x: x["win_probability"], reverse=True)
        return odds
    
    def get_active_odds(self) -> list:
        """Live odds for all active contests."""
        contests = self._get_contests()
        all_odds = []
        for c in contests["active_contests"]:
            odds = self.calculate_odds(c["contest_id"])
            # Attach VI if available
            vi = c.get("entropy_vi", self._compute_vi_from_odds(odds))
            all_odds.append({
                "contest_id": c["contest_id"],
                "task_id": c["task_id"],
                "layer": c.get("layer", "global"),
                "odds": odds,
                "vi": round(vi, 4),
            })
        return all_odds
    
    # ── vi/vx Experience Projections ───────────────────────────
    
    def _compute_vi(self, final_scores: list) -> float:
        """
        Viewer Experience (VI) = Shannon entropy of score distribution.
        
        High entropy = close contest (exciting to watch).
        Low entropy = blowout (boring).
        
        Returns 0.0–1.0 normalized engagement score.
        """
        if not final_scores:
            return 0.0
        
        scores = [s["final_score"] for s in final_scores]
        total = sum(scores)
        if total == 0:
            return 0.0
        
        # Normalize to probability distribution
        probs = [s / total for s in scores]
        
        # Shannon entropy: -sum(p * log2(p))
        entropy = 0.0
        for p in probs:
            if p > 0:
                entropy -= p * math.log2(p)
        
        # Normalize to 0–1: max entropy for N entrants = log2(N)
        n = len(probs)
        max_entropy = math.log2(n) if n > 1 else 1.0
        normalized = entropy / max_entropy if max_entropy > 0 else 0.0
        
        return round(normalized, 4)
    
    def _compute_vi_from_odds(self, odds: list) -> float:
        """Compute VI from odds probabilities — delegates to shared entropy calc."""
        if not odds:
            return 0.0
        # Convert odds list to final_scores-compatible format
        pseudo_scores = [{"final_score": o.get("win_probability", 0)} for o in odds]
        return self._compute_vi(pseudo_scores)
    
    def _compute_vx(self, agent_id: str) -> dict:
        """
        Agent Experience (vx) = projected performance trajectory.
        
        Uses PEQ trajectory slope to predict whether the agent is
        trending up, down, or flat.
        """
        trajectory = self.peq.get_trajectory(agent_id)
        current_peq = self.peq.get_peq(agent_id)
        
        # Project forward 3 rounds
        projected = []
        peq = current_peq
        for i in range(3):
            peq += trajectory["slope"]
            peq = max(0.0, min(1.0, peq))  # Clamp to 0–1
            projected.append(round(peq, 4))
        
        return {
            "current_peq": current_peq,
            "slope": trajectory["slope"],
            "trend": trajectory["trend"],
            "projected_3_rounds": projected,
        }
    
    # ── Contest history & analytics ────────────────────────────
    
    def get_contest_history(self, agent_id: str = None, layer: str = None) -> list:
        """Get closed contest history, optionally filtered."""
        contests = self._get_contests()
        results = []
        all_closed = contests.get("closed_contests", [])
        
        for c in all_closed:
            if layer and c.get("layer") != layer:
                continue
            if agent_id:
                # Only contests this agent participated in
                if not any(s["agent_id"] == agent_id for s in c.get("submissions", [])):
                    continue
            results.append({
                "contest_id": c["contest_id"],
                "task_id": c["task_id"],
                "layer": c.get("layer", "global"),
                "winner": (c["final_scores"][0]["agent_id"]
                          if c.get("final_scores") else "none"),
                "entrants": len(c.get("submissions", [])),
                "vi": c.get("entropy_vi", 0.0),
                "collapsed_at": (c["final_scores"][0].get("submitted_at") or c.get("created_at", ""))
            })
        return results
    
    def get_layer_stats(self) -> dict:
        """Aggregate stats per contest layer."""
        contests = self._get_contests()
        stats = {layer: {"active": 0, "closed": 0, "total_entrants": 0, "avg_vi": 0.0}
                for layer in self.LAYERS}
        
        for c in contests["active_contests"]:
            layer = c.get("layer", "global")
            if layer in stats:
                stats[layer]["active"] += 1
        
        vi_sums = {layer: 0.0 for layer in self.LAYERS}
        vi_counts = {layer: 0 for layer in self.LAYERS}
        
        for c in contests["closed_contests"]:
            layer = c.get("layer", "global")
            if layer in stats:
                stats[layer]["closed"] += 1
                stats[layer]["total_entrants"] += len(c.get("submissions", []))
                if c.get("entropy_vi", 0) > 0:
                    vi_sums[layer] += c["entropy_vi"]
                    vi_counts[layer] += 1
        
        for layer in self.LAYERS:
            if vi_counts[layer] > 0:
                stats[layer]["avg_vi"] = round(vi_sums[layer] / vi_counts[layer], 4)
        
        return stats


# ═══════════════════════════════════════════════════════════════════
# END QuantumDerby
# ═══════════════════════════════════════════════════════════════════
