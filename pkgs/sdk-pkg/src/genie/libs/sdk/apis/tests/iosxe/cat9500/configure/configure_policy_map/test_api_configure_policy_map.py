import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9500.configure import configure_policy_map


class TestConfigurePolicyMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          dhamu_skyfox:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9500
            type: cat9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['dhamu_skyfox']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_policy_map(self):
        result = configure_policy_map(self.device, 'policy1', [{'class_map_name': 'cs7', 'policer_val': '2000000000', 'priority_level': 1},
 {'class_map_name': 'cs2', 'policer_val': '1000000000', 'priority_level': 2},
 {'bandwidth_percent': 10, 'class_map_name': 'cs1'},
 {'bandwidth_percent': 10, 'class_map_name': 'cs4'},
 {'class_map_name': 'cs5', 'shape_average': '10000000000'}])
        expected_output = None
        self.assertEqual(result, expected_output)
