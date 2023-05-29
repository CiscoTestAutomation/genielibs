import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_bandwidth_remaining_policy_map


class TestConfigureBandwidthRemainingPolicyMap(unittest.TestCase):

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

    def test_configure_bandwidth_remaining_policy_map(self):
        result = configure_bandwidth_remaining_policy_map(self.device, ['parent', 'grandparent'], ['voice', 'data', 'video', 'class-default'], [20, 10, 10, 10, 30], '100')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_bandwidth_policy_map(self):
        result = configure_bandwidth_remaining_policy_map(self.device, ['parent', 'grandparent'], ['voice', 'data', 'video', 'class-default'], [7, 5, 5, 5], '100', bandwidth_remaining=False)
        expected_output = None
        self.assertEqual(result, expected_output)
