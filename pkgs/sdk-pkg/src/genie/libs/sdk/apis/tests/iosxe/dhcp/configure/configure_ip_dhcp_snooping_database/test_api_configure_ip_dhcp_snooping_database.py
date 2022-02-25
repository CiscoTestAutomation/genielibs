import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import configure_ip_dhcp_snooping_database


class TestConfigureIpDhcpSnoopingDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          SecG-A3-9410HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SecG-A3-9410HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_dhcp_snooping_database(self):
        result = configure_ip_dhcp_snooping_database(self.device, 'bootflash:dhcpsnoop.db', False, '10')
        expected_output = None
        self.assertEqual(result, expected_output)
