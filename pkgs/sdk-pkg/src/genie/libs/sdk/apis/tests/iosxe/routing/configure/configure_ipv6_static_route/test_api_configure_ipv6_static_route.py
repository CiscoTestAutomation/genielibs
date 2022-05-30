import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import configure_ipv6_static_route


class TestConfigureIpv6StaticRoute(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          VCR:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['VCR']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_static_route(self):
        result = configure_ipv6_static_route(self.device, '2001:16:1::0', 64, 'tunnel1', None)
        expected_output = None
        self.assertEqual(result, expected_output)
