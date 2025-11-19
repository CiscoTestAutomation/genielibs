from unittest import TestCase
from genie.libs.sdk.apis.iosxe.flexvpn.configure import configure_interface_virtual_template
from unittest.mock import Mock


class TestConfigureInterfaceVirtualTemplate(TestCase):

    def test_configure_interface_virtual_template(self):
        self.device = Mock()
        result = configure_interface_virtual_template(self.device, 200, 'tunnel', 'loopback', 100, None, None, 'IPSEC_PROFILE', False, '', True, None, False, None, None, None, None)
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Virtual-Template 200 type tunnel', 'ip unnumbered loopback 100', 'tunnel protection ipsec profile IPSEC_PROFILE', 'ipv6 enable'],)
        )
