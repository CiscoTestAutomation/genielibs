import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.execute import execute_test_sfp_port_lpn_fake_remove


class TestExecuteTestSfpPortLpnFakeRemove(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SA-C9350-24P:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SA-C9350-24P']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_test_sfp_port_lpn_fake_remove(self):
        result = execute_test_sfp_port_lpn_fake_remove(self.device, 'active', 1)
        expected_output = ''
        self.assertEqual(result, expected_output)
