import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor_filter_description


class TestConfigureBgpNeighborFilterDescription(unittest.TestCase):

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

    def test_configure_bgp_neighbor_filter_description(self):
        result = configure_bgp_neighbor_filter_description(self.device, 100, [{'as_id': 300,
  'damping_id': 1,
  'description': 'ibgp vers SWTDATA01',
  'filter_list': 1,
  'filter_routes': 'out',
  'mtu_discovery': 1,
  'neighbor_ip': '20.20.20.3',
  'neighbor_tag': 'externalpg',
  'soft_reconfiguration': 1}])
        expected_output = None
        self.assertEqual(result, expected_output)
