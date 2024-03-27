import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import unconfigure_dhcp_pool


class TestUnconfigureDhcpPool(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9200
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_dhcp_pool(self):
        result = unconfigure_dhcp_pool(self.device, 'vlan501', None, '1.1.1.0', '255.255.255.0', 'Mgmt-vrf', None)
        expected_output = None
        self.assertEqual(result, expected_output)
