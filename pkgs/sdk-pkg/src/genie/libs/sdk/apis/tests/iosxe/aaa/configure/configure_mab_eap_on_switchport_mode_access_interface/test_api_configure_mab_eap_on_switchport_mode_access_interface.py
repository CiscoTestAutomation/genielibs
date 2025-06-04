from unittest import TestCase
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_mab_eap_on_switchport_mode_access_interface
from unittest.mock import Mock


class TestConfigureAaaAuthorizationNetworkDefaultGroup(TestCase):

    def test_configure_mab_eap_on_switchport_mode_access_interface(self):
        self.device = Mock()
        configure_mab_eap_on_switchport_mode_access_interface(self.device, 'TenGigabitEthernet1/2/0/2')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface TenGigabitEthernet1/2/0/2', 'mab eap'],)
        )

