import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.execute import execute_install_one_shot


class TestExecuteInstallOneShot(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          AMZ-Acc-4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['AMZ-Acc-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_install_one_shot(self):
        result = execute_install_one_shot(self.device, 'tftp://172.27.18.5/auto/iconatest/users/byodis/images/cat9k_iosxe.17.10.01.SPA.bin', True, False, False, 900, 10, False, 'True')
        expected_output = False
        self.assertEqual(result, expected_output)
