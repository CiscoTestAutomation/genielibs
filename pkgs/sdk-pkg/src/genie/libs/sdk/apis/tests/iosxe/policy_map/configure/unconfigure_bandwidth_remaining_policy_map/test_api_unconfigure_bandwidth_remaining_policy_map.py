import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import unconfigure_bandwidth_remaining_policy_map


class TestUnconfigureBandwidthRemainingPolicyMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          BB_2HX:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['BB_2HX']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_bandwidth_remaining_policy_map(self):
        result = unconfigure_bandwidth_remaining_policy_map(self.device, ['parent', 'grandparent'])
        expected_output = None
        self.assertEqual(result, expected_output)
