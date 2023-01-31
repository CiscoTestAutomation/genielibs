import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup


class TestConfigureBgpNeighborRemoteAsFallOverAsWithPeergroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          mac-gen2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup(self):
        result = configure_bgp_neighbor_remote_as_fall_over_as_with_peergroup(self.device, '10', '1002:101::2', 'bfd', None, 'neigh-gig1')
        expected_output = None
        self.assertEqual(result, expected_output)
