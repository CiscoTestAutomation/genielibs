# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# Genie
from genie.libs.ops.interface.sonic.interface import Interface
from genie.libs.ops.interface.sonic.tests.interface_output import InterfaceOutput
from genie.libs.parser.sonic.show_interface import ShowInterfacesTransceiverEeprom

class test_platform_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='sonic')
        self.device.custom.setdefault("abstraction", {})["order"] = ["os", "platform"]
        self.device.mapping = {'cli': 'cli'}
        mock_connection = Mock()
        mock_connection.device = self.device
        self.device.connectionmgr.connections['cli'] = mock_connection

    def test_complete_output(self):
        self.maxDiff = None
        f = Interface(device=self.device)

        # Get outputs
        f.maker.outputs[ShowInterfacesTransceiverEeprom] = \
            {'':InterfaceOutput.show_interfaces_transceiver_eeprom}

        # Learn the feature
        f.learn()

        # Verify Ops was created successfully
        self.assertEqual(f.info, InterfaceOutput.showinterface_ops_output)

    def test_empty_parser_output(self):
        self.maxDiff = None
        f = Interface(device=self.device)

        # Get outputs
        f.maker.outputs[ShowInterfacesTransceiverEeprom] = {"": {}}

        # Learn the feature
        f.learn()

        # Check info was not created
        self.assertFalse(hasattr(f, 'info'))

if __name__ == '__main__':
    unittest.main()
