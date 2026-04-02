from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv6_object_group_network_entry


class TestUnconfigureIpv6ObjectGroupNetworkEntry(TestCase):

    def test_unconfigure_ipv6_object_group_network_entry(self):
        device = Mock()
        result = unconfigure_ipv6_object_group_network_entry(
            device=device,
            og_name='v6-srcnet-all',
            og_mode='host',
            ipv6_address='FE80::2A7:42FF:FE9B:D35F'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            (['object-group v6-network v6-srcnet-all', 'no host FE80::2A7:42FF:FE9B:D35F'],)
        )