import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nhrp.clear import monitor_event_trace_dmvpn_nhrp_clear


class TestMonitorEventTraceDmvpnNhrpClear(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          router1:
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
        self.device = self.testbed.devices['router1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_monitor_event_trace_dmvpn_nhrp_clear(self):
        result = monitor_event_trace_dmvpn_nhrp_clear(self.device, 30)
        expected_output = None
        self.assertEqual(result, expected_output)
