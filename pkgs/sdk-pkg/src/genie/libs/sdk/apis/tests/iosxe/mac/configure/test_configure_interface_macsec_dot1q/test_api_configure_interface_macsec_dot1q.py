from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.configure import configure_interface_macsec_dot1q


class TestConfigureInterfaceMacsecDot1Q(TestCase):

    def test_configure_interface_macsec_dot1q(self):
        self.device = Mock()
        interface = 'GigabitEthernet1/0/1'
        tag_number = 123

        configure_interface_macsec_dot1q(self.device, interface=interface, tag_number=tag_number)

        expected_commands = [
            f"interface {interface}",
            f"macsec dot1q {tag_number}",
        ]
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (expected_commands,)
        )
