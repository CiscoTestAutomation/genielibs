import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_ipv6_address_on_hsrp_interface


class TestConfigureIpv6AddressOnHsrpInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          platform-Prom-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['platform-Prom-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_address_on_hsrp_interface(self):
        result = configure_ipv6_address_on_hsrp_interface(self.device, 'Vlan600', 3, 2, '2001:db8:10::100/64', '100', '10', '10', '20')
        expected_output = None
        self.assertEqual(result, expected_output)
