import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.span.configure import unconfigure_local_span_filter


class TestUnconfigureLocalSpanFilter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch-9300:
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
        self.device = self.testbed.devices['Switch-9300']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_local_span_filter(self):
        result = unconfigure_local_span_filter(self.device, '1', 'vlan', '', '1')
        expected_output = None
        self.assertEqual(result, expected_output)
