import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.inventory.get import get_component_descr


class TestGetComponentDescr(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9600_Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9600_Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_component_descr(self):
        result = get_component_descr(self.device)
        expected_output = {'descr': ['Cisco Catalyst 9600 Series 6 Slot Chassis',
           'Cisco Catalyst 9600 Series 6 Slot Chassis Backplane',
           'Cisco Catalyst 9600 Series Carrier Card Module Container',
           'Cisco Catalyst 9600 Series Carrier Card Module Container',
           'Cisco Catalyst 9600 Series Carrier Card Module Container',
           'Cisco Catalyst 9600 Series Carrier Card Module Container',
           'Cisco Catalyst 9600 Series Carrier Card Module Container',
           'Cisco Catalyst 9600 Series Carrier Card Module Container',
           'Cisco Catalyst 9600 Series Routing Processor Module Container',
           'Supervisor 1 Module',
           'USB Port',
           'Hard Disk Container',
           'USB Port',
           'Network Management Ethernet',
           'Network Management TenGigEthernet',
           'Intel CPU x86-64',
           'Cisco Catalyst 9600 Series Routing Processor Module Container',
           'FAN t F0',
           'FAN t F1',
           'Cisco Catalyst 9600 Series Power Supply Bay Module Container',
           'Cisco Catalyst 9600 Series 2000W AC Power Supply',
           'Cisco Catalyst 9600 Series Power Supply',
           'FAN 1/1',
           'FAN 1/2',
           'Cisco Catalyst 9600 Series Power Supply Bay Module Container',
           'Cisco Catalyst 9600 Series 2000W AC Power Supply',
           'Cisco Catalyst 9600 Series Power Supply',
           'FAN 2/1',
           'FAN 2/2',
           'Cisco Catalyst 9600 Series Power Supply Bay Module Container',
           'Cisco Catalyst 9600 Series Power Supply Bay Module Container',
           'Cisco Catalyst 9600 Series Fan Tray Bay Module Container',
           'FAN Tray',
           'FAN 5/1',
           'FAN 5/2',
           'FAN 5/3',
           'FAN 5/4',
           'FAN 5/5',
           'FAN 5/6',
           'FAN 5/7',
           'FAN 5/8',
           'FAN 5/9'],
 'name': ['Chassis',
          'Backplane',
          'slot 1',
          'slot 2',
          'slot 3',
          'slot 4',
          'slot 5',
          'slot 6',
          'slot R0',
          'Slot 3 Supervisor',
          'Slot 3 - USB Port0',
          'Hard Disk Container R0',
          'Slot 3 - USB Port1',
          'Slot 3 - NME',
          'R0 - NMTGE',
          'Slot 3 CPU',
          'slot R1',
          'slot F0',
          'slot F1',
          'PowerSupplyContainer1',
          'PowerSupplyModule1',
          'PowerSupply1',
          'Fan1/1',
          'Fan1/2',
          'PowerSupplyContainer2',
          'PowerSupplyModule2',
          'PowerSupply2',
          'Fan2/1',
          'Fan2/2',
          'PowerSupplyContainer3',
          'PowerSupplyContainer4',
          'FanContainer',
          'FanTray',
          'Fan5/1',
          'Fan5/2',
          'Fan5/3',
          'Fan5/4',
          'Fan5/5',
          'Fan5/6',
          'Fan5/7',
          'Fan5/8',
          'Fan5/9']}
        self.assertEqual(result, expected_output)
