import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_rollback


class TestExecuteInstallRollback(unittest.TestCase):

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

    def test_execute_install_rollback(self):
        result = execute_install_rollback(self.device, 'base', None, False, None, 900, 10, True)
        expected_output = ('install_rollback: START Sun Aug 07 12:35:04 UTC 2022\r\n'
 'install_rollback: Rolling back to base\r\n'
 '--- Starting Rollback ---\r\n'
 'Performing Rollback on all members\r\n'
 ' [1] SMU_ROLLBACK package(s) on Switch 1\r\n'
 ' [3] SMU_ROLLBACK package(s) on Switch 3\r\n'
 ' [2] SMU_ROLLBACK package(s) on Switch 2\r\n'
 ' [2] Finished SMU_ROLLBACK package(s) on Switch 2\r\n'
 ' [3] Finished SMU_ROLLBACK package(s) on Switch 3\r\n'
 ' [1] Finished SMU_ROLLBACK package(s) on Switch 1\r\n'
 'Checking status of Rollback on [1 2 3]\r\n'
 'Rollback: Passed on [1 2 3]\r\n'
 'Finished Rollback operation\r\n'
 '\r\n'
 'SUCCESS: install_rollback Sun Aug 07 12:35:10 UTC 2022')
        self.assertEqual(result, expected_output)
