import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import configure_static_nat_route_map_no_alias_rule


class TestConfigureStaticNatRouteMapNoAliasRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyq-PE1:
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
        self.device = self.testbed.devices['stack3-nyq-PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_static_nat_route_map_no_alias_rule(self):
        result = configure_static_nat_route_map_no_alias_rule(self.device, 'inside', '192.168.1.10', '192.168.21.1', False)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_static_nat_route_map_no_alias_rule_1(self):
        result = configure_static_nat_route_map_no_alias_rule(self.device, 'outside', '3.3.33.3', '5.5.5.5', True)
        expected_output = None
        self.assertEqual(result, expected_output)
