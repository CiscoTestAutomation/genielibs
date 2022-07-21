import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.mcast.clear import clear_ip_mroute_vrf


class TestClearIpMrouteVrf(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          c2_core_sf:
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
        self.device = self.testbed.devices['c2_core_sf']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_ip_mroute_vrf(self):
        result = clear_ip_mroute_vrf(self.device, 'vn-5')
        expected_output = None
        self.assertEqual(result, expected_output)
