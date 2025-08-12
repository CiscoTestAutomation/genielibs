from unittest import TestCase
from genie.libs.sdk.apis.iosxe.cts.configure import configure_host_ip_to_sgt_mapping
from unittest.mock import Mock

class TestConfigureHostIpToSgtMapping(TestCase):

    def test_configure_host_ip_to_sgt_mapping(self):
        self.device = Mock()
        configure_host_ip_to_sgt_mapping(self.device, '3.3.3.3', 77)
        self.assertEqual(self.device.configure.mock_calls[0].args,("cts role-based sgt-map host 3.3.3.3 sgt 77",))


        
