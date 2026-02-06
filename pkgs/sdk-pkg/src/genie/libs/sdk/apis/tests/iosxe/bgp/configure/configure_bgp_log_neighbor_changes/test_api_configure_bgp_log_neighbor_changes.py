import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_log_neighbor_changes


class TestConfigureBgpLogNeighborChanges(unittest.TestCase):

    def test_configure_bgp_log_neighbor_changes(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_log_neighbor_changes(device, "100")
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ("router bgp 100\nbgp log-neighbor-changes\n",)
        )