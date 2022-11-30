import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import ping


class TestPing(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_ping(self):
        result = ping(self.device, '50.1.1.2', None, 1, None, 'af11', 256, 5, None, False, True, True, None, None, None, 'FFFFFFF')
        expected_output = {'ping': {'address': '50.1.1.2',
          'data_bytes': 256,
          'repeat': 5,
          'result_per_line': ['.....'],
          'statistics': {'received': 0, 'send': 5, 'success_rate_percent': 0.0},
          'timeout_secs': 1}}
        self.assertEqual(result, expected_output)
