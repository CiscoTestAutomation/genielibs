from unittest import TestCase
from genie.libs.sdk.apis.iosxe.dot1x.configure import unconfigure_dot1x_eap_profile_on_interface
from unittest.mock import Mock


class TestUnconfigureDot1xEapProfileOnInterface(TestCase):

    def test_unconfigure_dot1x_eap_profile_on_interface(self):
        self.device = Mock()
        result = unconfigure_dot1x_eap_profile_on_interface(self.device, 'GigabitEthernet2/0/1', 'EAPTLS-PROF-IOSCA', 'authenticator')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface GigabitEthernet2/0/1', 'no dot1x authenticator eap profile EAPTLS-PROF-IOSCA'],)
        )
