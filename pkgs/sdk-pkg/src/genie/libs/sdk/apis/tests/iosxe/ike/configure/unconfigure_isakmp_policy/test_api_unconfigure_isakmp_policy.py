import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import unconfigure_isakmp_policy


class TestUnconfigureIsakmpPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          INT1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['INT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_isakmp_policy(self):
        result = unconfigure_isakmp_policy(self.device, '666')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_isakmp_policy_1(self):
        result = unconfigure_isakmp_policy(self.device, '123')
        expected_output = None
        self.assertEqual(result, expected_output)
