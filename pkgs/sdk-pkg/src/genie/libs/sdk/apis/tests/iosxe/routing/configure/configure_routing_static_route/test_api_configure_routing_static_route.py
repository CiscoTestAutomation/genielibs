import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import configure_routing_static_route


class TestConfigureRoutingStaticRoute(unittest.TestCase):

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
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['R1_xe']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_routing_static_route(self):
        result = configure_routing_static_route(self.device, '10.1.1.0', '255.255.255.0', 'tunnel8', None, 'VRF1')
        expected_output = None
        self.assertEqual(result, expected_output)
