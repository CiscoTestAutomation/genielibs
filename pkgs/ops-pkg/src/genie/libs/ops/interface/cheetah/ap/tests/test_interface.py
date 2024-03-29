# Python
import unittest

# Ats
from pyats.topology import Device
from unittest.mock import Mock

# Genie
from genie.libs.ops.interface.cheetah.ap.interface import Interface
from genie.libs.ops.interface.cheetah.ap.tests.interface_output import InterfaceOutput
from genie.libs.parser.cheetah.show_interface import ShowInterfacesWired, \
                                                     ShowInterfacesDot11radio

outputs = {
    'show interfaces wired 0' : InterfaceOutput.showInterfaceWired_0,
    'show interfaces wired 1' : InterfaceOutput.showInterfaceWired_1,
    'show interfaces wired 2' : InterfaceOutput.showInterfaceWired_2,
    'show interfaces wired 3' : InterfaceOutput.showInterfaceWired_3,
    'show interfaces dot11radio 0' : InterfaceOutput.showInterfaceDot11Radio_0,
    'show interfaces dot11radio 1' : InterfaceOutput.showInterfaceDot11Radio_1,
    'show interfaces dot11radio 2' : InterfaceOutput.showInterfaceDot11Radio_2
}

def mapper(key):
    return outputs[key]

class test_platform_all(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice', os='cheetah', platform='ap')
        self.device.custom.setdefault("abstraction", {})["order"] = ["os", "platform"]
        self.device.mapping = {'cli': 'cli'}
        mock_connection = Mock()
        mock_connection.device = self.device
        self.device.connectionmgr.connections['cli'] = mock_connection
        mock_connection.execute.side_effect = mapper

    def test_complete_output(self):
        self.maxDiff = None
        f = Interface(device=self.device)

        # Learn the feature
        f.learn()

        # Verify Ops was created successfully
        self.assertEqual(f.info, InterfaceOutput.showinterface_ops_output)

    def test_empty_parser_output(self):
        self.maxDiff = None
        f = Interface(device=self.device)

        # Get outputs
        outputs["show interfaces wired 0"] = ''
        outputs["show interfaces wired 1"] = ''
        outputs["show interfaces wired 2"] = ''
        outputs["show interfaces wired 3"] = ''
        outputs["show interfaces dot11radio 0"] = ''
        outputs["show interfaces dot11radio 1"] = ''
        outputs["show interfaces dot11radio 2"] = ''

        # Learn the feature
        f.learn()

        # Check info was not created
        self.assertFalse(hasattr(f, 'info'))

if __name__ == '__main__':
    unittest.main()

