from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv6_object_group_network


class TestUnconfigureIpv6ObjectGroupNetwork(TestCase):

    def test_unconfigure_ipv6_object_group_network(self):
        device = Mock()
        result = unconfigure_ipv6_object_group_network(
            device=device,
            og_name='v6-srcnet-all'
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('no object-group v6-network v6-srcnet-all',)
        )