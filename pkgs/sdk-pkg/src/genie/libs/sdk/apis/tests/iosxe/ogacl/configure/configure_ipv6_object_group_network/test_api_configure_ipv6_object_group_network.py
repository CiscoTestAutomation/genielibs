from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv6_object_group_network

class TestConfigureIpv6ObjectGroupNetwork(TestCase):

    def test_configure_ipv6_object_group_network(self):
        device = Mock()
        result = configure_ipv6_object_group_network(
            device=device,
            og_name='v6-srcnet-all-2',
            og_mode='network',
            ipv6_address='',
            ipv6_network='2013:1:1::',
            prefix='64'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['object-group v6-network v6-srcnet-all-2', '2013:1:1::/64'],)
        )