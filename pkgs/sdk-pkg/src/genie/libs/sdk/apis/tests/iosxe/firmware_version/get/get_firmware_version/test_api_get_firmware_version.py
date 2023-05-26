import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.firmware_version.get import get_firmware_version


class TestGetFirmwareVersion(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          mac2-sjc24:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac2-sjc24']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_firmware_version(self):
        result = get_firmware_version(self.device)
        expected_output = {'firmware_version': [['17050302'],
                      ['17.10.1r',
                       '17.10.1r',
                       '(7.3, 7.0, 6.0)',
                       '(7.3, 7.0, 6.0)',
                       '17.10.1r',
                       '17.10.1r',
                       '17.10.1r']],
 'name': [['FanTray'],
          ['Slot 3 Supervisor',
           'Slot 4 Supervisor',
           'PowerSupplyModule5',
           'PowerSupplyModule8',
           'Slot 1 Linecard',
           'Slot 6 Linecard',
           'Slot 7 Linecard']]}
        self.assertEqual(result, expected_output)
