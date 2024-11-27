import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.debug.configure import set_platform_soft_trace_ptp_debug


class TestSetPlatformSoftTracePtpDebug(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Gryphon:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Gryphon']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_set_platform_soft_trace_ptp_debug(self):
        result = set_platform_soft_trace_ptp_debug(self.device, 'fed', 'active', 'ptp_proto', 'debug', None)
        expected_output = None
        self.assertEqual(result, expected_output)
