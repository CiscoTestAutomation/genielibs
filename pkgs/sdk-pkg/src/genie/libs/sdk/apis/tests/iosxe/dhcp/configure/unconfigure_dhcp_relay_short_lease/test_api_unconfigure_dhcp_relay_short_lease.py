import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_relay_short_lease


class TestUnconfigureDhcpRelayShortLease(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          BB_1HX:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['BB_1HX']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_dhcp_relay_short_lease(self):
        result = unconfigure_dhcp_relay_short_lease(self.device, 60, False)
        expected_output = None
        self.assertEqual(result, expected_output)
