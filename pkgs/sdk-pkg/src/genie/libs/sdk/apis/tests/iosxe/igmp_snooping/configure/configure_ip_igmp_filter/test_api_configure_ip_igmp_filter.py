from unittest import TestCase
from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import configure_ip_igmp_filter
from unittest.mock import Mock


class TestConfigureIpIgmpFilter(TestCase):

    def test_configure_ip_igmp_filter(self):
        self.device = Mock()
        result = configure_ip_igmp_filter(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('ip igmp filter',)
        )
