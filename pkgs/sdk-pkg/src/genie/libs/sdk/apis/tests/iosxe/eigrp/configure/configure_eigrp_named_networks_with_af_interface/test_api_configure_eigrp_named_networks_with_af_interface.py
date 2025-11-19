from unittest import TestCase
from genie.libs.sdk.apis.iosxe.eigrp.configure import configure_eigrp_named_networks_with_af_interface
from unittest.mock import Mock


class TestConfigureEigrpNamedNetworksWithAfInterface(TestCase):

    def test_configure_eigrp_named_networks_with_af_interface(self):
        self.device = Mock()
        result = configure_eigrp_named_networks_with_af_interface(self.device, 'EIGRP_NAME3', 300, ['10.0.0.0'], '255.255.255.0', '10.0.0.1', 'ipv4', '', 'unicast', 'TwoGigabitEthernet0/0/1', False, True, False)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['router eigrp EIGRP_NAME3', 'address-family ipv4 unicast autonomous-system 300', 'network 10.0.0.0 255.255.255.0', 'eigrp router-id 10.0.0.1', 'af-interface TwoGigabitEthernet0/0/1', 'bfd', 'passive-interface', 'no split-horizon', 'no shutdown', 'exit-af-interface'],)
        )
