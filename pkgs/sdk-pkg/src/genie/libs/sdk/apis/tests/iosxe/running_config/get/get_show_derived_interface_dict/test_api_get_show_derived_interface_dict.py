import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.running_config.get import get_show_derived_interface_dict


class TestGetShowDerivedInterfaceDict(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr1:
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
        self.device = self.testbed.devices['kparames_csr1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_show_derived_interface_dict(self):
        result = get_show_derived_interface_dict(self.device, 'Tunnel1')
        expected_output = {'derived_config': {'Tunnel1': {'ip_access_group_in': 'Tu1-ipsec-ds-ipv4-in',
                                'ip_access_group_out': 'Tu1-ipsec-ds-ipv4-out',
                                'ip_address': '192.168.1.1',
                                'ipv6': 'enabled',
                                'ipv6_access_group_in': 'Tu1-ipsec-ds-ipv6-in',
                                'ipv6_access_group_out': 'Tu1-ipsec-ds-ipv6-out',
                                'tunnel_destination': '30.30.30.2',
                                'tunnel_ipsec_profile': 'prof',
                                'tunnel_mode': 'ipsec dual-overlay',
                                'tunnel_source': 'GigabitEthernet1'}}}
        self.assertEqual(result, expected_output)
