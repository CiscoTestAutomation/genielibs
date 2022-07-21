import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.aireos.get import get_boot_variables


class TestGetBootVariables(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          vWLC:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os aireos --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: aireos
            platform: single_rp
            type: ap
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['vWLC']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_boot_variables(self):
        result = get_boot_variables(self.device)
        expected_output = ({'status': 'active', 'version': '8.10.151.0'}, {'version': '8.10.151.0'})
        self.assertEqual(result, expected_output)
