from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_serial_physical_layer
from unittest.mock import Mock


class TestConfigureInterfaceSerialPhysicalLayer(TestCase):

    def test_configure_interface_serial_physical_layer(self):
        self.device = Mock()
        result = configure_interface_serial_physical_layer(self.device, 'Serial 0/3/0', 'async')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Serial 0/3/0', 'physical-layer async'],)
        )
