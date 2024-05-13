import unittest
from unittest.mock import MagicMock
from python2 import closeWindow  

class TestCloseWindow(unittest.TestCase):
    def test_close_window(self):
        mock_window = MagicMock()
        closeWindow(mock_window)
        mock_window.destroy.assert_called_once()

