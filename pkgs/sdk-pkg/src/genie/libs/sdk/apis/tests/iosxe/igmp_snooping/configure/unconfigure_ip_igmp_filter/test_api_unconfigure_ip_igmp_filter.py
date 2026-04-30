from unittest import TestCase
from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import unconfigure_ip_igmp_filter
from unittest.mock import Mock


class TestUnconfigureIpIgmpFilter(TestCase):

    def test_unconfigure_ip_igmp_filter(self):
        self.device = Mock()
        result = unconfigure_ip_igmp_filter(self.device)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no ip igmp filter',)
        )
