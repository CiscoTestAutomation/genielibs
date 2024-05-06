import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.running_config.get import get_running_config_dict


class TestGetRunningConfigDict(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          r1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8kv
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['r1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_running_config_dict(self):
        result = get_running_config_dict(self.device)
        expected_output = {
            'aaa authentication login default local': {},
            'aaa authorization exec default local': {},
            'aaa new-model': {},
            'aaa session-id common': {},
        }
        self.assertEqual(result, expected_output)
