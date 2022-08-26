import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.install.verify import verify_install_state


class TestVerifyInstallState(unittest.TestCase):

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

    def test_verify_install_state(self):
        result = verify_install_state(self.device, 'SMU', 'C')
        expected_output = True
        self.assertEqual(result, expected_output)
