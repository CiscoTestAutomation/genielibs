import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import configure_nat_pool


class TestConfigureNatPool(unittest.TestCase):

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

    def test_configure_nat_pool(self):
        result = configure_nat_pool(self.device, 'outside_pool', '4.4.4.4', '4.5.5.5', '255.0.0.0', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_nat_pool_1(self):
        result = configure_nat_pool(self.device, 'outside_pool1', '4.4.4.4', '4.5.5.5', None, 8)
        expected_output = None
        self.assertEqual(result, expected_output)
