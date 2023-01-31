import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_policy_map_type_service


class TestConfigurePolicyMapTypeService(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          UUT1:
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
        self.device = self.testbed.devices['UUT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_policy_map_type_service(self):
        result = configure_policy_map_type_service(self.device, 'map1', None)
        expected_output = None
        self.assertEqual(result, expected_output)
