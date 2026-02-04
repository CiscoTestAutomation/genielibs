from unittest import TestCase
from genie.libs.sdk.apis.iosxe.mpls.configure import unconfigure_mpls_static_binding_ipv4
from unittest.mock import Mock


class TestUnconfigureMplsStaticBindingIpv4(TestCase):

    def test_unconfigure_mpls_static_binding_ipv4(self):
        self.device = Mock()
        result = unconfigure_mpls_static_binding_ipv4(self.device, '10.2.2.0', '255.255.255.255', None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ('no mpls static binding ipv4 10.2.2.0 255.255.255.255',)
        )
