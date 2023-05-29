import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.logging.configure import unconfigure_logging


class TestUnconfigureLogging(unittest.TestCase):

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
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_logging(self):
        result = unconfigure_logging(self.device, 'on', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_logging_1(self):
        result = unconfigure_logging(self.device, 'console', 6)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_logging_2(self):
        result = unconfigure_logging(self.device, 'buffered', 'critical')
        expected_output = None
        self.assertEqual(result, expected_output)
