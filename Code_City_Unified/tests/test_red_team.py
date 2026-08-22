
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: os, red_team, sys, unittest
# ROLE: Test positive identification of an open port
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

import red_team

class TestRedTeamScanner(unittest.TestCase):

    @patch('red_team.socket.socket')
    def test_port_scan_open(self, mock_socket_cls):
        """Test positive identification of an open port"""
        # Setup mock socket
        mock_socket = MagicMock()
        mock_socket_cls.return_value.__enter__.return_value = mock_socket
        
        # Connect returns None on success (port open)
        mock_socket.connect.return_value = None
        
        result = red_team.port_scan("localhost", 80)
        self.assertTrue(result)

    @patch('red_team.socket.socket')
    def test_port_scan_closed(self, mock_socket_cls):
        """Test handling of a closed port (ConnectionRefusedError)"""
        # Setup mock socket to raise error
        mock_socket = MagicMock()
        mock_socket_cls.return_value.__enter__.return_value = mock_socket
        mock_socket.connect.side_effect = ConnectionRefusedError
        
        result = red_team.port_scan("localhost", 80)
        self.assertFalse(result)

    @patch('red_team.socket.socket')
    def test_port_scan_timeout(self, mock_socket_cls):
        """Test handling of a timeout"""
        import socket
        mock_socket = MagicMock()
        mock_socket_cls.return_value.__enter__.return_value = mock_socket
        mock_socket.connect.side_effect = socket.timeout
        
        result = red_team.port_scan("localhost", 80)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
