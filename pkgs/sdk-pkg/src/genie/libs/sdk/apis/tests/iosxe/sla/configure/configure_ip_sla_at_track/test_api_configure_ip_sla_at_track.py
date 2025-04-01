from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sla.configure import configure_ip_sla_at_track
from unittest.mock import Mock


class TestConfigureIpSlaAtTrack(TestCase):

    def test_configure_ip_sla_at_track(self):
        self.device = Mock()
        result = configure_ip_sla_at_track(self.device, 2147483647, 32767)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('track 32767 ip sla 2147483647',)
        )
