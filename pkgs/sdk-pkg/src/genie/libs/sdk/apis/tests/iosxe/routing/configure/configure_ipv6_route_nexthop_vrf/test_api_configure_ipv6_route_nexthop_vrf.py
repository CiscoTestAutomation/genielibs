import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import configure_ipv6_route_nexthop_vrf


class TestConfigureIpv6RouteNexthopVrf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Stargazer:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Stargazer']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_route_nexthop_vrf(self):
        result = configure_ipv6_route_nexthop_vrf(self.device, '2009::/64', 'TenGigabitEthernet2/2/0/35', 'vrf1')
        expected_output = None
        self.assertEqual(result, expected_output)
