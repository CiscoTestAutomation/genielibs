import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.get import get_RIPng_routes


class TestGetRipngRoutes(unittest.TestCase):

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

    def test_get_RIPng_routes(self):
        result = get_RIPng_routes(self.device)
        expected_output = ['800:12:22::/64']
        self.assertEqual(result, expected_output)
