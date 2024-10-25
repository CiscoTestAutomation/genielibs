import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_class_map.configure import configure_traffic_class_for_class_map


class TestConfigureTrafficClassForClassMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Raitt:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Raitt']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_traffic_class_for_class_map(self):
        result = configure_traffic_class_for_class_map(self.device, 'tc7', 'match-any', 7)
        expected_output = None
        self.assertEqual(result, expected_output)
