import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_snooping_information_option_allow_untrusted


class TestConfigureIpDhcpSnoopingInformationOptionAllowUntrusted(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          access:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['access']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_dhcp_snooping_information_option_allow_untrusted(self):
        result = configure_ip_dhcp_snooping_information_option_allow_untrusted(self.device, 'Port-channel 93')
        expected_output = None
        self.assertEqual(result, expected_output)
