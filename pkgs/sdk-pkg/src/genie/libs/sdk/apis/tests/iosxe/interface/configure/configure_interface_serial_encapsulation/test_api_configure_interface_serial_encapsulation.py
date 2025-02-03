from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_serial_encapsulation
from unittest.mock import Mock


class TestConfigureInterfaceSerialEncapsulation(TestCase):

    def test_configure_interface_serial_encapsulation(self):
        self.device = Mock()
        result = configure_interface_serial_encapsulation(self.device, 'Serial 0/3/0', 'raw-tcp')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Serial 0/3/0', 'encapsulation raw-tcp'],)
        )
