import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.get import get_bgp_route_ext_community


class TestGetBgpRouteExtCommunity(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          R1_xe:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: csr1000v
            type: CSR1000v
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_bgp_route_ext_community(self):
        result = get_bgp_route_ext_community(self.device, 'VPNv4', '3.3.3.3', 'VRF1')
        expected_output = None
        self.assertEqual(result, expected_output)
