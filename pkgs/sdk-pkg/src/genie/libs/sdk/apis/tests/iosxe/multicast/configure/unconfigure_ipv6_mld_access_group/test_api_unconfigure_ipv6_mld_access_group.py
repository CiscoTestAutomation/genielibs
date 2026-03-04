from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ipv6_mld_access_group

class TestUnconfigureIpv6MldAccessGroup(TestCase):

    def test_unconfigure_ipv6_mld_access_group(self):
        device = Mock()
        result = unconfigure_ipv6_mld_access_group(device, 'te1/0/1', None)
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['int te1/0/1', 'no ipv6 mld access-group None'],)
        )