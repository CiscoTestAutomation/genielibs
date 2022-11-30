import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.platform.execute import execute_delete_files


class TestExecuteDeleteFiles(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Steller-QSA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: nxos
            platform: n9k
            type: Nexus9000
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Steller-QSA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_delete_files(self):
        result = execute_delete_files(self.device, 'bootflash', 'nxos.9.4.1.IJB9.0.622.bin', 300)
        expected_output = None
        self.assertEqual(result, expected_output)
