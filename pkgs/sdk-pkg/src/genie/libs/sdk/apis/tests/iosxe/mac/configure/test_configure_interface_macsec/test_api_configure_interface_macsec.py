from unittest import TestCase
from unittest.mock import Mock
from genie.libs.sdk.apis.iosxe.mac.configure import configure_interface_macsec, unconfigure_interface_macsec


class TestConfigureInterfaceMacsec(TestCase):

    def test_configure_interface_macsec(self):
        self.device = Mock()
        interface = "GigabitEthernet1/0/1"

        configure_interface_macsec(self.device, interface=interface)

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface {}".format(interface), "macsec"],)
        )

    def test_unconfigure_interface_macsec(self):
        self.device = Mock()
        interface = "GigabitEthernet1/0/1"

        unconfigure_interface_macsec(self.device, interface=interface)

        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (["interface {}".format(interface), "no macsec"],)
        )
