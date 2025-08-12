from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_ip_to_sgt_mapping_vrf
from unittest.mock import Mock

class TestConfigureIpToSgtMappingVrf(TestCase):

    def test_configure_ip_to_sgt_mapping_vrf(self):
        self.device = Mock()
        configure_ip_to_sgt_mapping_vrf(self.device, 'cisco', '4.4.4.4', 77)
        self.assertEqual(self.device.configure.mock_calls[0].args, ('cts role-based sgt-map vrf cisco 4.4.4.4 sgt 77',))

