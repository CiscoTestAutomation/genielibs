from unittest import TestCase
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_access_group
from unittest.mock import Mock


class TestUnconfigureIpIgmpAccessGroup(TestCase):

    def test_unconfigure_ip_igmp_access_group(self):
        self.device = Mock()
        result = unconfigure_ip_igmp_access_group(self.device, 'FiftyGigE1/0/1', 'IGMP-GROUP-FILTER')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface FiftyGigE1/0/1', 'no ip igmp access-group IGMP-GROUP-FILTER'],)
        )
