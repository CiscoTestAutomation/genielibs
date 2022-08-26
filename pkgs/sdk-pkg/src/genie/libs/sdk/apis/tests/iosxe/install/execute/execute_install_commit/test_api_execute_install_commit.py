import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_commit


class TestExecuteInstallCommit(unittest.TestCase):

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

    def test_execute_install_commit(self):
        result = execute_install_commit(self.device)
        expected_output = ('install_commit: START Sun Aug 07 09:04:03 UTC 2022\r\n'
 '--- Starting Commit ---\r\n'
 'Performing Commit on all members\r\n'
 ' [1] Commit packages(s) on Switch 1\r\n'
 ' [2] Commit packages(s) on Switch 2\r\n'
 ' [3] Commit packages(s) on Switch 3\r\n'
 ' [2] Finished Commit packages(s) on Switch 2\r\n'
 ' [1] Finished Commit packages(s) on Switch 1\r\n'
 ' [3] Finished Commit packages(s) on Switch 3\r\n'
 'Checking status of Commit on [1 2 3]\r\n'
 'Commit: Passed on [1 2 3]\r\n'
 'Finished Commit operation\r\n'
 '\r\n'
 'SUCCESS: install_commit')
        self.assertEqual(result, expected_output)
