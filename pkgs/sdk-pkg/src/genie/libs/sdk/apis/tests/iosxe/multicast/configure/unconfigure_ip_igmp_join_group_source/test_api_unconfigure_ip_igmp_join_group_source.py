from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_join_group_source

class TestUnconfigureIpIgmpJoinGroupSource(TestCase):

    def test_unconfigure_ip_igmp_join_group_source(self):
        device = Mock()
        result = unconfigure_ip_igmp_join_group_source(device, 'te1/0/1', '226.1.1.1', '')
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['interface te1/0/1', 'no ip igmp join-group 226.1.1.1'],)
        )