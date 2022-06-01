import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import unconfigure_routing_static_route


class TestUnconfigureRoutingStaticRoute(unittest.TestCase):

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

    def test_unconfigure_routing_static_route(self):
        result = unconfigure_routing_static_route(self.device, '64', 'CLIENT-VRFv4', 'tunnel20', None)
        expected_output = None
        self.assertEqual(result, expected_output)
