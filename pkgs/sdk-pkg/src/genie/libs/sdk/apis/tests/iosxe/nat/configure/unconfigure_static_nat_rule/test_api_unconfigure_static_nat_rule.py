import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_static_nat_rule


class TestUnconfigureStaticNatRule(unittest.TestCase):

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

    def test_unconfigure_static_nat_rule(self):
        result = unconfigure_static_nat_rule(self.device, '193.168.0.2', '10.10.10.1', 'tcp', 22, 22, True, 'VRF2', True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_static_nat_rule_1(self):
        result = unconfigure_static_nat_rule(self.device, '193.168.0.2', '10.10.10.1', None, None, None, True, 'VRF2', True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_static_nat_rule_2(self):
        result = unconfigure_static_nat_rule(self.device, '193.168.0.2', '10.10.10.1', 'tcp', 22, 22, False, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)
