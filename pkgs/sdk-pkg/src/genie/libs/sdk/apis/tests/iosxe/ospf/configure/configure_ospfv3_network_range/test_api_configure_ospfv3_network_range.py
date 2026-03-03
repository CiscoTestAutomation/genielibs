from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospfv3_network_range
from unittest.mock import Mock


class TestConfigureOspfv3NetworkRange(TestCase):

    def test_configure_ospfv3_network_range(self):
        self.device = Mock()
        result = configure_ospfv3_network_range(self.device, '100', '1.1.1.1', 'ipv6', 'unicast', 'True', '1', '2010::/64', 'True')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router ospfv3 100', 'router-id 1.1.1.1', 'log-adjacency-changes', 'address-family ipv6 unicast', 'area 1 range 2010::/64', 'bfd all-interfaces'],)
        )
