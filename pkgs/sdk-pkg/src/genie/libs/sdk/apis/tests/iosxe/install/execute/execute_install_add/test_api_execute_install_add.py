import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_add


class TestExecuteInstallAdd(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PI-9300-Stack-103:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PI-9300-Stack-103']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_install_add(self):
        result = execute_install_add(self.device, 'bootflash:cat9k_iosxe.2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin', True, False, 900, 10)
        expected_output = ('$22-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin\r\n'
 'install_add: START Sun Aug 07 12:13:49 UTC 2022\r\n'
 'install_add: Adding IMG\r\n'
 ' [1] Switch 1 Add succeed with reason: SMU Already Added-No Change\r\n'
 ' [2] Switch 2 Add succeed with reason: SMU Already Added-No Change\r\n'
 ' [3] Switch 3 Add succeed with reason: SMU Already Added-No Change\r\n'
 'SUCCESS: install_add')
        self.assertEqual(result, expected_output)
