from unittest import TestCase
from genie.libs.sdk.apis.iosxe.sla.configure import configure_ip_sla_schedule
from unittest.mock import Mock


class TestConfigureIpSlaSchedule(TestCase):

    def test_configure_ip_sla_schedule(self):
        self.device = Mock()
        result = configure_ip_sla_schedule(self.device, 2147483647, 20, 'Forever', 'Now', True)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip sla schedule 2147483647 life Forever start-time Now ageout 20 recurring',)
        )
