import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.qos.configure import config_policy_map_on_interface


class TestConfigPolicyMapOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Startrek:
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
        self.device = self.testbed.devices['Startrek']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_policy_map_on_interface(self):
        result = config_policy_map_on_interface(self.device, 'Fou2/0/20', 'map-1')
        expected_output = None
        self.assertEqual(result, expected_output)
