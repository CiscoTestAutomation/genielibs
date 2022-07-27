import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.get import get_ipv6_connected_routes


class TestGetIpv6ConnectedRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          uut:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iol
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['uut']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_ipv6_connected_routes(self):
        result = get_ipv6_connected_routes(self.device)
        expected_output = ['2001::/64',
 '2001:4::/64',
 '3000:1::/64',
 '3000:2::/64',
 '3000:4::/64',
 '3200:1::/64']
        self.assertEqual(result, expected_output)
