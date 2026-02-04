import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_refresh_max_eor_time


class TestConfigureBgpRefreshMaxEorTime(unittest.TestCase):

    def test_configure_bgp_refresh_max_eor_time(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_refresh_max_eor_time(device, 5001, 600)
        self.assertIsNone(result)

        self.assertEqual(
            device.configure.mock_calls[0].args,
            ("router bgp 5001\nbgp sso route-refresh-enable\nbgp refresh max-eor-time 600\n",)
        )