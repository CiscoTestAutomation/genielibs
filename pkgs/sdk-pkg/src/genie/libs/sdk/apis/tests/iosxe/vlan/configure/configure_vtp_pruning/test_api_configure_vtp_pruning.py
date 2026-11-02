from unittest import TestCase
from unittest.mock import Mock

from genie.libs.sdk.apis.iosxe.vlan.configure import configure_vtp_pruning


class TestConfigureVtpPruning(TestCase):

    def test_configure_vtp_pruning(self):
        device = Mock()
        result = configure_vtp_pruning(device)

        self.assertIsNone(result)
        device.configure.assert_called_once_with('vtp pruning')
