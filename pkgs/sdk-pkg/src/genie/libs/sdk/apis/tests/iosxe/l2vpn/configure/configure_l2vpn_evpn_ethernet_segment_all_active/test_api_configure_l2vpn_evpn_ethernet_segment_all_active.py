import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.l2vpn.configure import configure_l2vpn_evpn_ethernet_segment_all_active


class TestConfigureL2vpnEvpnEthernetSegmentAllActive(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          R1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_l2vpn_evpn_ethernet_segment_all_active(self):
        result = configure_l2vpn_evpn_ethernet_segment_all_active(self.device, 1, 3, '0012.0012.0012', 1)
        expected_output = None
        self.assertEqual(result, expected_output)
