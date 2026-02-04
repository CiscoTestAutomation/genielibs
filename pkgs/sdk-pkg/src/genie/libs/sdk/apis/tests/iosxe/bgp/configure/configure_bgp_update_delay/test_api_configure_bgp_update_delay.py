import unittest
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_update_delay


class TestConfigureBgpUpdateDelay(unittest.TestCase):

    def test_configure_bgp_update_delay(self):
        device = Mock()
        device.configure.return_value = ""

        result = configure_bgp_update_delay(device, 1, 1)
        self.assertIsNone(result)

        # Update if your API uses a different CLI format (string vs list)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ([
                "router bgp 1",
                "bgp update-delay 1",
            ],)
        )