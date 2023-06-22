import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.evpn.configure import configure_evpn_ethernet_segment


class TestConfigureEvpnEthernetSegment(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
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
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_evpn_ethernet_segment(self):
        result = configure_evpn_ethernet_segment(self.device, 6, 0, None, '00.00.00.00.00.00.00.00.01', True)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_evpn_ethernet_segment_1(self):
        result = configure_evpn_ethernet_segment(self.device, 7, 3, '00.00.00', None, False)
        expected_output = None
        self.assertEqual(result, expected_output)
