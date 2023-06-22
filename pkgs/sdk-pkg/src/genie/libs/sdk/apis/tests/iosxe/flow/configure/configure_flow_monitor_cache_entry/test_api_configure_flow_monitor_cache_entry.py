import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.flow.configure import configure_flow_monitor_cache_entry


class TestConfigureFlowMonitorCacheEntry(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Starfleet:
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
        self.device = self.testbed.devices['Starfleet']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_flow_monitor_cache_entry(self):
        result = configure_flow_monitor_cache_entry(self.device, 'dnacmonitor', 'dnacrecord', 10, None, 'dnacexporter')
        expected_output = None
        self.assertEqual(result, expected_output)
