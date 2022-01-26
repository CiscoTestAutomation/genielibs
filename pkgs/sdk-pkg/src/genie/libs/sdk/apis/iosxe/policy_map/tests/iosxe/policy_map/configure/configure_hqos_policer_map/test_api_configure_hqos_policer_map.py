import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_hqos_policer_map


class TestConfigureHqosPolicerMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Startek:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Startek']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_hqos_policer_map(self):
        result = configure_hqos_policer_map(device=self.device, policy_name='policy2', class_map_name='class-default', policer_percent_val=1, table_map_name='table1', table_map_mode='dscp', child_policy='policy1', match_mode=['dscp', 'cos'], matched_value=['cs1', '5'])
        expected_output = None
        self.assertEqual(result, expected_output)
