import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_abort


class TestExecuteInstallAbort(unittest.TestCase):

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

    def test_execute_install_abort(self):
        result = execute_install_abort(self.device)
        expected_output = ('install_abort: START Sun Aug 07 12:19:18 UTC 2022\r\n'
 '--- Starting Abort ---\r\n'
 'Performing Abort on all members\r\n'
 ' [1] SMU_ABORT packages(s) on Switch 1\r\n'
 ' [3] SMU_ABORT packages(s) on Switch 3\r\n'
 ' [2] SMU_ABORT packages(s) on Switch 2\r\n'
 ' [2] Finished SMU_ABORT packages(s) on Switch 2\r\n'
 ' [3] Finished SMU_ABORT packages(s) on Switch 3\r\n'
 ' [1] Finished SMU_ABORT packages(s) on Switch 1\r\n'
 'Checking status of Abort on [1 2 3]\r\n'
 'Abort: Passed on [1 2 3]\r\n'
 'Finished Abort operation\r\n'
 '\r\n'
 'SUCCESS: install_abort Sun Aug 07 12:19:25 UTC 2022')
        self.assertEqual(result, expected_output)
