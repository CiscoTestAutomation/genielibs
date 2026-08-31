import unittest
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_vtp_pruning


class TestUnconfigureVtpPruning(unittest.TestCase):

    def test_unconfigure_vtp_pruning(self):
        device = Mock()

        result = unconfigure_vtp_pruning(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('no vtp pruning')
