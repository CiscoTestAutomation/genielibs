from unittest import TestCase
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_serial_physical_layer
from unittest.mock import Mock


class TestUnconfigureInterfaceSerialPhysicalLayer(TestCase):

    def test_unconfigure_interface_serial_physical_layer(self):
        self.device = Mock()
        result = unconfigure_interface_serial_physical_layer(self.device, 'Serial 0/3/0', 'async')
        self.assertEqual(
            self.device.configure.mock_calls[0].args,
            (['interface Serial 0/3/0', 'no physical-layer async'],)
        )
