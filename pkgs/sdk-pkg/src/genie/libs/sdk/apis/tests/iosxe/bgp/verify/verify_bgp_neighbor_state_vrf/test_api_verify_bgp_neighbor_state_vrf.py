import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.verify import verify_bgp_neighbor_state_vrf


class TestVerifyBgpNeighborStateVrf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          P-R1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['P-R1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_bgp_neighbor_state_vrf(self):
        result = verify_bgp_neighbor_state_vrf(self.device, 'vpnv4', 'unicast', 'client1-vrf', '10.1.1.2', '2', 60, 20)
        expected_output = True
        self.assertEqual(result, expected_output)
