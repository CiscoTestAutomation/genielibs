import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.table_map.configure import configure_table_map_set_default


class TestConfigureTableMapSetDefault(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9400-ha:
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
        self.device = self.testbed.devices['9400-ha']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_table_map_set_default(self):
        result = configure_table_map_set_default(self.device, 'cos2cos', 'copy')
        expected_output = None
        self.assertEqual(result, expected_output)
