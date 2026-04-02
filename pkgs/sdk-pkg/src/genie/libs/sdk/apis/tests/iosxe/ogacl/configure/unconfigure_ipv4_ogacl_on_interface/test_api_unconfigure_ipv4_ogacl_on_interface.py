from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.ogacl.configure import unconfigure_ipv4_ogacl_on_interface


class TestUnconfigureIpv4OgaclOnInterface(TestCase):

    def test_unconfigure_ipv4_ogacl_on_interface(self):
        device = Mock()
        result = unconfigure_ipv4_ogacl_on_interface(
            device,
            'TenGigabitEthernet7/0/4',
            'ogacl_policy_in',
            True
        )
        self.assertEqual(result, None)
        self.assertEqual(
            device.configure.mock_calls[0].args,
              ('interface TenGigabitEthernet7/0/4\nno ip access-group ogacl_policy_in in',)
        )