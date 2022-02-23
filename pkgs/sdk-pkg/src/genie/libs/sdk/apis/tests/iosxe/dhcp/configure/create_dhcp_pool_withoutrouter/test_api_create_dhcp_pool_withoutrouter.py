import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dhcp.configure import create_dhcp_pool_withoutrouter


class TestCreateDhcpPoolWithoutrouter(unittest.TestCase):

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

    def test_create_dhcp_pool_withoutrouter(self):
        result = create_dhcp_pool_withoutrouter(self.device, 'VLAN_10', '10.10.10.0', '255.255.255.0', '0', '0', '35')
        expected_output = None
        self.assertEqual(result, expected_output)
