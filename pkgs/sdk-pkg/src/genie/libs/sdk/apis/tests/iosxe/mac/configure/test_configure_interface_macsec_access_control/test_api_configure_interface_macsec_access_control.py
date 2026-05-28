from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.configure import configure_interface_macsec_access_control


class TestConfigureInterfaceMacsecAccessControl(TestCase):

    def test_configure_interface_macsec_access_control(self):
        self.device = Mock()
        interface = 'GigabitEthernet1/0/1'
        mode = 'always-accept'

        configure_interface_macsec_access_control(self.device, interface=interface, mode=mode)

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            ([
                f'interface {interface}',
                f'macsec access-control {mode}',
            ],)
        )
