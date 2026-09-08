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


class LadderMode(unittest.TestCase):
    def setUp(self):
        self.arena = Arena()

    def test_rungs_escalate_in_strength(self):
        run = self.arena.create_ladder(
            "viper", "VIPER", "spaghetti_untangle",
            ["PUNK", "SOLDIER", "WARLORD"], base_elo=1200, rung_gap=50)
        elos = [o["elo"] for o in run.opponents]
        self.assertEqual(elos, [1200, 1250, 1300])
        self.assertTrue(run.ladder)

    def test_ladder_bonus_scales_per_rung(self):
        run = self.arena.create_ladder(
            "viper", "VIPER", "spaghetti_untangle",
            ["PUNK", "SOLDIER", "WARLORD"])
        self.arena.start_ladder_ = run  # keep reference
        self.arena.start_gauntlet(run.id)
        self.arena._score_challenger = lambda run, code, t: 999
        self.arena._score_opponent = lambda challenge, loadout: 1
        for _ in range(3):
            self.arena.submit_gauntlet(run.id, SOLUTION)
        # 3 rungs: bonus = 10 * (1+2+3) = 60, on top of 3 ELO wins
        self.assertGreater(self.arena.leaderboard["viper"],
                           1200 + 60)

    def test_ladder_vs_flat_gauntlet_bonus(self):
        # same 3 opponents: ladder pays 60 bonus, flat gauntlet pays 30
        ladder = self.arena.create_ladder(
            "climber", "CLIMBER", "spaghetti_untangle",
            ["A", "B", "C"])
        flat = self.arena.create_gauntlet(
            "stander", "STANDER", "spaghetti_untangle",
            [("x", "A"), ("y", "B"), ("z", "C")])
        self.arena.start_gauntlet(ladder.id)
        self.arena.start_gauntlet(flat.id)
        self.arena._score_challenger = lambda run, code, t: 999
        self.arena._score_opponent = lambda challenge, loadout: 1
        for _ in range(3):
            self.arena.submit_gauntlet(ladder.id, SOLUTION)
            self.arena.submit_gauntlet(flat.id, SOLUTION)
        # both get the same 3 ELO wins; the ladder's climbing bonus is
        # strictly larger than the flat sweep bonus
        self.assertGreater(self.arena.leaderboard["climber"],
                           self.arena.leaderboard["stander"])

    def test_loss_ends_the_climb(self):
        run = self.arena.create_ladder(
            "viper", "VIPER", "spaghetti_untangle", ["PUNK", "SOLDIER"])
        self.arena.start_gauntlet(run.id)
        self.arena._score_challenger = lambda run, code, t: 50
        self.arena._score_opponent = lambda challenge, loadout: 100
        r = self.arena.submit_gauntlet(run.id, SOLUTION)
        self.assertFalse(r["fight"]["challenger_won"])
        self.assertEqual(r["status"], "lost")
        again = self.arena.submit_gauntlet(run.id, SOLUTION)
        self.assertIn("error", again)


class BrownRuling(unittest.TestCase):
    """Brown's post-match audit hits the scoreboard: solo teams that
    should have united pay ELO per ghost; clean teams don't."""

    def setUp(self):
        self.arena = Arena()
        self.arena.leaderboard["viper"] = 1200
        self.arena.leaderboard["ravage"] = 1200
        self.arena.leaderboard["bastion"] = 1200

    def _fake_brown(self, red_ghosts, blue_ghosts):
        class _Brown:
            pass

        b = _Brown()
        b.solo_red = {"side": "red", "ghosts": red_ghosts}
        b.solo_blue = {"side": "blue", "ghosts": blue_ghosts}
        b.unify_or_get_humped = ("UNITE — the chain walks only when the "
                                 "ledgers are one")
        return b

    def test_solo_sides_pay_for_ghosts(self):
        intel = {"brown": self._fake_brown(red_ghosts=10, blue_ghosts=0)}
        res = self.arena.apply_brown_verdict(
            intel, {"red": ["viper", "ravage"], "blue": ["bastion"]})
        # red refused to unite: 10 ghosts -> 10 ELO off each red player
        self.assertEqual(self.arena.leaderboard["viper"], 1190)
        self.assertEqual(self.arena.leaderboard["ravage"], 1190)
        # blue walked it clean solo — nothing to answer for
        self.assertEqual(self.arena.leaderboard["bastion"], 1200)
        self.assertIn("red", res["penalties"])
        self.assertNotIn("blue", res["penalties"])

    def test_no_brown_no_penalty(self):
        res = self.arena.apply_brown_verdict(
            {}, {"red": ["viper"], "blue": ["bastion"]})
        self.assertEqual(res["ruling"], "no audit")
        self.assertEqual(self.arena.leaderboard["viper"], 1200)

    def test_penalty_capped_for_long_engagements(self):
        intel = {"brown": self._fake_brown(red_ghosts=500, blue_ghosts=0)}
        self.arena.apply_brown_verdict(
            intel, {"red": ["viper"], "blue": ["bastion"]})
        # capped at 40 — a long war doesn't zero a team
        self.assertEqual(self.arena.leaderboard["viper"], 1200 - 40)
        self.assertEqual(self.arena.leaderboard["bastion"], 1200)

    def test_clean_engagement_no_penalties(self):
        intel = {"brown": self._fake_brown(red_ghosts=0, blue_ghosts=0)}
        res = self.arena.apply_brown_verdict(
            intel, {"red": ["viper"], "blue": ["bastion"]})
        self.assertEqual(res["penalties"], {})
        self.assertEqual(self.arena.leaderboard["viper"], 1200)
        self.assertEqual(self.arena.leaderboard["bastion"], 1200)


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