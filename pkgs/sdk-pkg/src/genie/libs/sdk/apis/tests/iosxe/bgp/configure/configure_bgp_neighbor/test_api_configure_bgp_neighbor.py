import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_bgp_neighbor


class TestConfigureBgpNeighbor(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr9:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            model: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['kparames_csr9']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_bgp_neighbor(self):
        result = configure_bgp_neighbor(self.device, '64001', '64002', '192.168.1.2', 'Gig8', None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_bgp_neighbor_1(self):
        result = configure_bgp_neighbor(self.device, '64001', '64002', '192.168.1.2', 'Gig8', None, 'ipv4', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_bgp_neighbor_2(self):
        result = configure_bgp_neighbor(self.device, '64001', '64002', '192.168.1.2', 'Gig8', None, 'ipv4', 'test')
        expected_output = None
        self.assertEqual(result, expected_output)
