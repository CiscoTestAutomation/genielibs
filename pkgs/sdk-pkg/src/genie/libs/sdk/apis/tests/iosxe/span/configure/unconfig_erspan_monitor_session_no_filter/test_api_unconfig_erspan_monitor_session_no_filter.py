import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.span.configure import unconfig_erspan_monitor_session_no_filter


class TestUnconfigErspanMonitorSessionNoFilter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Franklin-9300L-Stack:
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
        self.device = self.testbed.devices['Franklin-9300L-Stack']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_erspan_monitor_session_no_filter(self):
        result = unconfig_erspan_monitor_session_no_filter(self.device, '1', '2333')
        expected_output = None
        self.assertEqual(result, expected_output)
