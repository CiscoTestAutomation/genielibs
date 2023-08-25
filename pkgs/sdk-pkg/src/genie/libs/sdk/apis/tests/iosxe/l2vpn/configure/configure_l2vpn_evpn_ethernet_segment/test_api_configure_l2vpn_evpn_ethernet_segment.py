import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.l2vpn.configure import configure_l2vpn_evpn_ethernet_segment


class TestConfigureL2vpnEvpnEthernetSegment(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500L
            type: c9500L
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_l2vpn_evpn_ethernet_segment(self):
        result = configure_l2vpn_evpn_ethernet_segment(self.device, 201, 3, 'aaaa.201b.201c', 1)
        expected_output = None
        self.assertEqual(result, expected_output)
