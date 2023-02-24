import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map


class TestConfigurePolicyMap(unittest.TestCase):

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

    def test_configure_policy_map(self):
        result = configure_policy_map(
            device=self.device,
            policy_name='policy1', 
            class_map_list=[
                {
                    'class_map_name': 'test1',
                    'match_mode': ['dscp', 'cos'],
                    'matched_value': ['cs2', '5'],
                    'policer_val': 20000000000
                },
                {
                    'class_map_name': 'test2',
                    'match_mode': ['cos'],
                    'matched_value': ['2'],
                    'policer_val': 20000000000
                },
                {
                    'class_map_name': 'class-default',
                    'policer_val': 20000000000,
                    'table_map_mode': 'cos',
                    'table_map_name': 'table_cos'
                }
            ]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
