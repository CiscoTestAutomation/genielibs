from unittest import TestCase
from genie.libs.sdk.apis.iosxe.autovpn.configure import configure_virtual_template_for_autovpn
from unittest.mock import Mock


class TestConfigureVirtualTemplateForAutovpn(TestCase):

    def test_configure_virtual_template_for_autovpn(self):
        self.device = Mock()
        result = configure_virtual_template_for_autovpn(self.device, 1, 'ipsec_profile_autovpn', None, 'ipsec ipv4')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Virtual-Template1 type tunnel', 'no ip address', 'tunnel mode ipsec ipv4', 'tunnel protection ipsec profile ipsec_profile_autovpn'],)
        )
