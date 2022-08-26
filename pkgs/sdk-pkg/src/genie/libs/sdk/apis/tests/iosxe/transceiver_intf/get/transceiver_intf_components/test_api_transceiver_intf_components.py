import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.transceiver_intf.get import transceiver_intf_components


class TestTransceiverIntfComponents(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          nyquist3-sjc24:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
            custom:
              abstraction:
                order: [os, type]
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['nyquist3-sjc24']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_transceiver_intf_components(self):
        result = transceiver_intf_components(self.device)
        expected_output = {'connector_type': ['openconfig-transport-types:LC_CONNECTOR'],
 'form_factor': ['openconfig-transport-types:SFP'],
 'serial_no': ['AVD212292NK'],
 'transceiver': ['TenGigabitEthernet1/1/6'],
 'vendor_name': ['CISCO-AVAGO'],
 'vendor_part': ['SFBR-709SMZ-CS1'],
 'vendor_rev': ['G4.1']}
        self.assertEqual(result, expected_output)
