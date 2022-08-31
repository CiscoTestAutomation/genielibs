import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.verify import verify_bgp_l2vpn_evpn_rt2_nxthop


class TestVerifyBgpL2vpnEvpnRt2Nxthop(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          leaf1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9300
            type: cat9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['leaf1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_bgp_l2vpn_evpn_rt2_nxthop(self):
        result = verify_bgp_l2vpn_evpn_rt2_nxthop(self.device, '3.3.3.3:1', '3.3.3.3', '2000::23', 30, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
