from unittest import TestCase
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_address_advertisement
from  unittest.mock import Mock

class TestConfigureBgpAddressAdvertisement(TestCase):

    def test_configure_bgp_address_advertisement(self):
        self.device = Mock()
        configure_bgp_address_advertisement(self.device, '65004', 'ipv4', '1.1.1.1', '255.255.255.255', 'WAN-VRF')
        self.device.configure.assert_called_with(['router bgp 65004', 'address-family ipv4 vrf WAN-VRF', 'network 1.1.1.1 mask 255.255.255.255'])

