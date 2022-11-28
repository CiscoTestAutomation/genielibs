import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_ip_route_cache


class TestUnconfigureIpRouteCache(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          3850-48P:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['3850-48P']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_route_cache(self):
        result = unconfigure_ip_route_cache(self.device, 'GigabitEthernet2/0/17')
        expected_output = None
        self.assertEqual(result, expected_output)
