import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import unconfigure_static_nat_outside_rule


class TestUnconfigureStaticNatOutsideRule(unittest.TestCase):

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

    def test_unconfigure_static_nat_outside_rule(self):
        result = unconfigure_static_nat_outside_rule(self.device, '193.168.128.2', '20.20.20.1', 'tcp', 34, 34, True, '255.255.0.0', True, True, 'VRF2')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_static_nat_outside_rule_1(self):
        result = unconfigure_static_nat_outside_rule(self.device, '193.168.128.2', '20.20.20.1', None, None, None, False, None, True, True, 'VRF2')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_static_nat_outside_rule_2(self):
        result = unconfigure_static_nat_outside_rule(self.device, '193.168.128.2', '20.20.20.1', 'tcp', 34, 34, False, None, False, False, 'VRF2')
        expected_output = None
        self.assertEqual(result, expected_output)
