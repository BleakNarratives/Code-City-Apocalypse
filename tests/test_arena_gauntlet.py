#!/usr/bin/env python3

# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-src
# DEPS: arena, random, sys, unittest
# ROLE: Tests for the 1-vs-N gauntlet challenge mode in the Arena.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-09-08 SCOUT_CONTAINER + gauntlet session
# TIER: Test (0)
# [/DNA_TAG]

"""Tests for the Arena's gauntlet mode — one challenger vs N opponents.

The challenger declares how many they're worth. Fought sequentially:
lose once and the run is over; beat the whole line and it's a sweep
(legend status + ELO bonus).
"""

from __future__ import annotations

import random
import sys
import unittest
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from src.buildings.arena import Arena, GauntletRun  # noqa: E402

SOLUTION = 'def solve(data):\n    """clean solution"""\n    return sorted(data)\n'
OPPONENTS = [("equinex", "EQUINEX"), ("lidarr", "LIDARR"),
             ("bastion", "BASTION")]


class GauntletBasics(unittest.TestCase):
    def setUp(self):
        self.arena = Arena()

    def test_create_gauntlet_declares_opponents(self):
        run = self.arena.create_gauntlet(
            "viper", "VIPER", "spaghetti_untangle", OPPONENTS)
        self.assertIsInstance(run, GauntletRun)
        self.assertEqual(len(run.opponents), 3)
        self.assertEqual(run.status, "pending")
        self.assertIn("gauntlet_", run.id)

    def test_unknown_challenge_rejected(self):
        with self.assertRaises(ValueError):
            self.arena.create_gauntlet(
                "viper", "VIPER", "no_such_challenge", OPPONENTS)

    def test_empty_opponent_line_rejected(self):
        with self.assertRaises(ValueError):
            self.arena.create_gauntlet(
                "viper", "VIPER", "spaghetti_untangle", [])

    def test_submit_before_start_refused(self):
        run = self.arena.create_gauntlet(
            "viper", "VIPER", "spaghetti_untangle", OPPONENTS[:1])
        res = self.arena.submit_gauntlet(run.id, SOLUTION)
        self.assertIn("error", res)


class GauntletFightOrder(unittest.TestCase):
    def setUp(self):
        self.arena = Arena()
        self.run = self.arena.create_gauntlet(
            "viper", "VIPER", "spaghetti_untangle", OPPONENTS)
        self.arena.start_gauntlet(self.run.id)

    def test_opponents_fought_in_declared_order(self):
        random.seed(7)
        fought = []
        for _ in range(len(OPPONENTS)):
            res = self.arena.submit_gauntlet(self.run.id, SOLUTION)
            fought.append(res["fight"]["opponent_name"])
        self.assertEqual(fought, ["EQUINEX", "LIDARR", "BASTION"])

    def test_sweep_awards_legend_and_elo_bonus(self):
        random.seed(7)
        for _ in range(len(OPPONENTS)):
            self.arena.submit_gauntlet(self.run.id, SOLUTION)
        # 3 opponents swept: 3 ELO wins + 3*10 sweep bonus over base 1200
        self.assertGreater(self.arena.leaderboard["viper"], 1200)
        self.assertEqual(self.run.status, "won")

    def test_loss_ends_run_no_continuation(self):
        # deterministic: the line is strictly stronger
        self.arena._score_challenger = lambda run, code, t: 50
        self.arena._score_opponent = lambda challenge, loadout: 100
        res = self.arena.submit_gauntlet(self.run.id, SOLUTION)
        self.assertFalse(res["fight"]["challenger_won"])
        self.assertEqual(self.run.status, "lost")
        # the line refuses a rematch — the run is over
        again = self.arena.submit_gauntlet(self.run.id, SOLUTION)
        self.assertIn("error", again)

    def test_tie_counts_as_loss(self):
        # equal scores: the challenger must BEAT the line, not tie it
        self.arena._score_challenger = lambda run, code, t: 100
        self.arena._score_opponent = lambda challenge, loadout: 100
        res = self.arena.submit_gauntlet(self.run.id, SOLUTION)
        self.assertEqual(res["fight"]["challenger_score"], 100)
        self.assertEqual(res["fight"]["opponent_score"], 100)
        self.assertFalse(res["fight"]["challenger_won"])


class GauntletLedger(unittest.TestCase):
    def test_finished_runs_move_to_history(self):
        arena = Arena()
        run = arena.create_gauntlet(
            "viper", "VIPER", "spaghetti_untangle", OPPONENTS[:1])
        arena.start_gauntlet(run.id)
        random.seed(7)
        arena.submit_gauntlet(run.id, SOLUTION)
        self.assertNotIn(run.id, arena.active_matches)
        self.assertTrue(any(getattr(h, "id", "") == run.id
                            for h in arena.match_history))

    def test_stats_recorded_for_challenger_and_line(self):
        arena = Arena()
        run = arena.create_gauntlet(
            "viper", "VIPER", "spaghetti_untangle", OPPONENTS[:1])
        arena.start_gauntlet(run.id)
        random.seed(7)
        arena.submit_gauntlet(run.id, SOLUTION)
        stats = arena.player_stats["viper"]
        self.assertEqual(stats["wins"], 1)
        self.assertEqual(stats["matches_played"], 1)


if __name__ == "__main__":
    unittest.main()