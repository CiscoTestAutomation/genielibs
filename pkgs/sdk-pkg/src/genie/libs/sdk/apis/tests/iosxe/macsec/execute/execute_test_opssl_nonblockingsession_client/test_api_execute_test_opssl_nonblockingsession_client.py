import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.macsec.execute import execute_test_opssl_nonblockingsession_client


class TestExecuteTestOpsslNonblockingsessionClient(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          MSFT_9500H_SPINE:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['MSFT_9500H_SPINE']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_test_opssl_nonblockingsession_client(self):
        result = execute_test_opssl_nonblockingsession_client(self.device, 'tls1.2', '192.168.1.1', '9001', '1', '10', '2048', '0', 'client', 'client')
        expected_output = None
        self.assertEqual(result, expected_output)
