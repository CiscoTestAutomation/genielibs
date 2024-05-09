import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import disable_dhcp_smart_relay


class TestDisableDhcpSmartRelay(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          rep-sw2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['rep-sw2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_disable_dhcp_smart_relay(self):
        result = disable_dhcp_smart_relay(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
