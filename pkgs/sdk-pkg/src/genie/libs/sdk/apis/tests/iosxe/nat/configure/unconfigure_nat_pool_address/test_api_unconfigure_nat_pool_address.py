import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_nat_pool_address


class TestUnconfigureNatPoolAddress(unittest.TestCase):

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

    def test_unconfigure_nat_pool_address(self):
        result = unconfigure_nat_pool_address(self.device, 'inside_pool1', '1.1.1.1', '1.2.2.2', '255.0.0.0', None, 'match-host')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_nat_pool_address_1(self):
        result = unconfigure_nat_pool_address(self.device, 'inside_pool2', '1.1.1.1', '1.2.2.2', None, 8, None)
        expected_output = None
        self.assertEqual(result, expected_output)
