from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_timers
from unittest.mock import Mock


class TestConfigureBgpTimers(TestCase):

    def test_configure_bgp_timers(self):
        self.device = Mock()
        result = configure_bgp_timers(self.device, 200, 30, 90)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router bgp 200', 'timers bgp 30 90'],)
        )
