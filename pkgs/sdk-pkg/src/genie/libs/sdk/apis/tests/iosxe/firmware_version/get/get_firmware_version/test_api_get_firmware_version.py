import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.firmware_version.get import get_firmware_version


class TestGetFirmwareVersion(unittest.TestCase):

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

    def test_get_firmware_version(self):
        result = get_firmware_version(self.device)
        expected_output = {'firmware_version': [[],
                      ['NULL',
                       'NULL',
                       '(N/A, N/A, N/A)',
                       '(N/A, N/A, N/A)',
                       '17.8.1r']],
 'name': [[],
          ['Slot 3 Supervisor',
           'FanTray',
           'PowerSupplyModule1',
           'PowerSupplyModule2',
           'Slot 1 Linecard']]}
        self.assertEqual(result, expected_output)
