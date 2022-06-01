import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.pbr.configure import configure_route_map_under_interface


class TestConfigureRouteMapUnderInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Galaga-4:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Galaga-4']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_route_map_under_interface(self):
        result = configure_route_map_under_interface(self.device, 'Fi1/0/5', 'rm_v4pbr_nexthop1', False)
        expected_output = None
        self.assertEqual(result, expected_output)
