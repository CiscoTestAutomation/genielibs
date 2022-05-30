import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import unconfigure_routing_static_routev6


class TestUnconfigureRoutingStaticRoutev6(unittest.TestCase):

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

    def test_unconfigure_routing_static_routev6(self):
        result = unconfigure_routing_static_routev6(self.device, '24:1::2', '64', 'CLIENT-VRF1v6', 'tunnel20', '25:1::2')
        expected_output = None
        self.assertEqual(result, expected_output)
