from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import configure_mpls_static_binding_ipv4
from unittest.mock import Mock


class TestConfigureMplsStaticBindingIpv4(TestCase):

    def test_configure_mpls_static_binding_ipv4(self):
        self.device = Mock()
        result = configure_mpls_static_binding_ipv4(self.device, '10.2.2.0', '255.255.255.255', 'input 31')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('mpls static binding ipv4 10.2.2.0 255.255.255.255 input 31',)
        )
