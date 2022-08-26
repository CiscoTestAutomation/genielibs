import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_deactivate


class TestExecuteInstallDeactivate(unittest.TestCase):

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

    def test_execute_install_deactivate(self):
        result = execute_install_deactivate(self.device, None, True, False, 'flash:cat9k_iosxe.2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin', 900, 10)
        expected_output = ('$.2022-06-06_12.21_mcpre.24042.CSCvq24042.SSA.smu.bin \r\n'
 'install_deactivate: START Sun Aug 07 12:30:18 UTC 2022\r\n'
 'install_deactivate: Deactivating\r\n'
 '--- Starting SMU Deactivate operation ---\r\n'
 'Performing SMU_DEACTIVATE on all members\r\n'
 'Checking status of SMU_DEACTIVATE on [1 2 3]\r\n'
 'SMU_DEACTIVATE: Passed on [1 2 3]\r\n'
 'Finished SMU Deactivate operation\r\n'
 '\r\n'
 'SUCCESS: install_deactivate Sun Aug 07 12:30:33 UTC 2022')
        self.assertEqual(result, expected_output)
