import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.transceiver_intf.get import transceiver_intf_components


class TestTransceiverIntfComponents(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          full3d2_dut2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            custom:
              abstraction:
                order: [os, model]
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['full3d2_dut2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_transceiver_intf_components(self):
        result = transceiver_intf_components(self.device)
        expected_output = {'connector_type': ['openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR',
                    'openconfig-transport-types:LC_CONNECTOR'],
 'form_factor': ['openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP',
                 'openconfig-transport-types:SFP'],
 'serial_no': ['AVD2325DB0V',
               'AVD221799E2',
               'AVD221799EV',
               'AVD221799ED',
               'AVD221799EB',
               'AVD21309XZY',
               'FNS20221ADK',
               'OPM22140NMM',
               'AVD221699CN',
               'AVD221799E8'],
 'transceiver': ['TenGigabitEthernet1/4/0/9',
                 'TenGigabitEthernet1/4/0/33',
                 'TenGigabitEthernet1/4/0/34',
                 'TenGigabitEthernet1/4/0/35',
                 'TenGigabitEthernet1/4/0/36',
                 'TenGigabitEthernet2/4/0/13',
                 'TenGigabitEthernet2/4/0/33',
                 'TenGigabitEthernet2/4/0/34',
                 'TenGigabitEthernet2/4/0/35',
                 'TenGigabitEthernet2/4/0/36'],
 'vendor_name': ['CISCO-AVAGO',
                 'CISCO-AVAGO',
                 'CISCO-AVAGO',
                 'CISCO-AVAGO',
                 'CISCO-AVAGO',
                 'CISCO-AVAGO',
                 'CISCO-FINISAR',
                 'CISCO-OPLINK',
                 'CISCO-AVAGO',
                 'CISCO-AVAGO'],
 'vendor_part': ['SFBR-709SMZ-CS2',
                 'SFBR-709SMZ-CS1',
                 'SFBR-709SMZ-CS1',
                 'SFBR-709SMZ-CS1',
                 'SFBR-709SMZ-CS1',
                 'SFBR-709SMZ-CS1',
                 'FTLX8571D3BCL-C2',
                 'TPP4XGDS0CCISE2G',
                 'SFBR-709SMZ-CS1',
                 'SFBR-709SMZ-CS1'],
 'vendor_rev': ['G4.1',
                'G4.1',
                'G4.1',
                'G4.1',
                'G4.1',
                'G4.1',
                'A',
                '01',
                'G4.1',
                'G4.1']}
        self.assertEqual(result, expected_output)
