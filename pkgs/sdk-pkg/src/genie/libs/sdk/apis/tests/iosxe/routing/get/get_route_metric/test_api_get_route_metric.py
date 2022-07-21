import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.get import get_route_metric


class TestGetRouteMetric(unittest.TestCase):

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

    def test_get_route_metric(self):
        result = get_route_metric(self.device)
        expected_output = {'2001:4::/64': 0,
 '2001:4::201/128': 0,
 '2001::/64': 0,
 '2001::1/128': 0,
 '3000:1::/64': 0,
 '3000:1::1/128': 0,
 '3000:2::/64': 0,
 '3000:2::1/128': 0,
 '3000:4::/64': 0,
 '3000:4::1/128': 0,
 '3200:1::/64': 0,
 '3200:1::1/128': 0,
 'AAAA::/64': 10,
 'FF00::/8': 0}
        self.assertEqual(result, expected_output)
