import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.inventory.get import get_hardware_version


class TestGetHardwareVersion(unittest.TestCase):

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

    def test_get_hardware_version(self):
        result = get_hardware_version(self.device)
        expected_output = {'hardware_version': [[],
                      ['V01',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'V02',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'V01',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'V01',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'V01',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL',
                       'NULL']],
 'name': [[],
          ['Chassis',
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
           'Fan5/9']]}
        self.assertEqual(result, expected_output)
