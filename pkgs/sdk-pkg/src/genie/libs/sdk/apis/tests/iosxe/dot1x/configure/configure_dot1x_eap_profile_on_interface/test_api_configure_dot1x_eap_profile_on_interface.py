from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_dot1x_eap_profile_on_interface
from unittest.mock import Mock


class TestConfigureDot1xEapProfileOnInterface(TestCase):

    def test_configure_dot1x_eap_profile_on_interface(self):
        self.device = Mock()
        result = configure_dot1x_eap_profile_on_interface(self.device, 'GigabitEthernet2/0/1', 'EAPTLS-PROF-IOSCA', 'supplicant')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet2/0/1', 'dot1x supplicant eap profile EAPTLS-PROF-IOSCA'],)
        )
