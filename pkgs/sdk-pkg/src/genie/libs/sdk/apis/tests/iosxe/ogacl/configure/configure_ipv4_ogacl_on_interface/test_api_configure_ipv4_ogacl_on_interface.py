from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import configure_ipv4_ogacl_on_interface

class TestConfigureIpv4OgaclOnInterface(TestCase):

    def test_configure_ipv4_ogacl_on_interface(self):
        device = Mock()
        result = configure_ipv4_ogacl_on_interface(
            device, 'TenGigabitEthernet7/0/4', 'ogacl_policy_in', True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
            ('interface TenGigabitEthernet7/0/4\nip access-group ogacl_policy_in in',)
        )