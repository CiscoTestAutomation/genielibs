import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.configure import force_unconfigure_static_nat_route_map_rule


class TestForceUnconfigureStaticNatRouteMapRule(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Stargazer:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Stargazer']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_force_unconfigure_static_nat_route_map_rule(self):
        result = force_unconfigure_static_nat_route_map_rule(self.device, '35.0.0.1', '135.0.0.1', 'rm1', 60)
        expected_output = None
        self.assertEqual(result, expected_output)
