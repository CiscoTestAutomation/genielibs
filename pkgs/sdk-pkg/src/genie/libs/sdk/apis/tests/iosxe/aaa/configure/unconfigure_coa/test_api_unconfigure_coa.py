import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.aaa.configure import unconfigure_coa


class TestUnconfigureCoa(unittest.TestCase):

    def test_unconfigure_coa(self):
        self.device = Mock()
        unconfigure_coa(self.device)
        self.device.configure.assert_called_with([
            'no aaa server radius dynamic-author'
        ])
