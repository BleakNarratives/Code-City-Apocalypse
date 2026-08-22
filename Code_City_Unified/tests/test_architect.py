
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: modmind_architect, os, sys, unittest
# ROLE: Test that 'battle' keyword triggers the battle protocol
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Test (0)
# [/DNA_TAG]

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the source directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../modmind_unified/src')))

import modmind_architect

class TestModMindArchitect(unittest.TestCase):

    @patch('modmind_architect.titan_battle')
    def test_routing_battle(self, mock_battle):
        """Test that 'battle' keyword triggers the battle protocol"""
        modmind_architect.modmind_architect("Start a battle simulation")
        mock_battle.run_battle.assert_called_once()

    @patch('modmind_architect.red_team')
    def test_routing_red_team(self, mock_red_team):
        """Test that 'scan' keyword triggers the red team protocol"""
        modmind_architect.modmind_architect("run scan on localhost")
        mock_red_team.run_recon_scan.assert_called_once()

    @patch('modmind_architect.red_team')
    def test_target_extraction(self, mock_red_team):
        """Test that the architect correctly extracts the target hostname"""
        modmind_architect.modmind_architect("scan target google.com")
        # Verify call args
        args, _ = mock_red_team.run_recon_scan.call_args
        self.assertEqual(args[0], "google.com")

    @patch('modmind_architect.logging')
    def test_unknown_command(self, mock_logging):
        """Test fallback for unknown commands"""
        modmind_architect.modmind_architect("bake a cake")
        # Check if the specific info log was called
        found_log = False
        for call in mock_logging.info.call_args_list:
            if "Task not recognized" in str(call):
                found_log = True
                break
        self.assertTrue(found_log, "Should log that task was not recognized")

if __name__ == '__main__':
    unittest.main()
