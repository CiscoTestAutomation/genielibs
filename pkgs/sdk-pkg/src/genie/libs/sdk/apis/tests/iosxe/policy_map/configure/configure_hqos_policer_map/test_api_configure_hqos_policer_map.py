import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.policy_map.configure import configure_hqos_policer_map


class TestConfigureHqosPolicerMap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          NGSVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['NGSVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_hqos_policer_map(self):
        result = configure_hqos_policer_map(self.device, 'cs3', 'tc7', '5', None, None, None, None, None, None, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)
