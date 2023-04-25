import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.get import get_outgoing_interface_with_vrf


class TestGetOutgoingInterfaceWithVrf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          iolpe2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_outgoing_interface_with_vrf(self):
        result = get_outgoing_interface_with_vrf(self.device, '100.8.9.0', 'default')
        expected_output = [['100.3.5.5', 'default', 'Ethernet3/1', 'i L2'],
 ['100.3.4.4', 'default', 'Ethernet5/1', 'i L2'],
 ['99.3.5.5', 'default', 'Ethernet3/0', 'i L2'],
 ['99.3.4.4', 'default', 'Ethernet5/0', 'i L2']]
        self.assertEqual(result, expected_output)
