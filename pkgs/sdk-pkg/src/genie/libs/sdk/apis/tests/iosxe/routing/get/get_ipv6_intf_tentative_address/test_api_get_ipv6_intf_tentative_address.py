import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.get import get_ipv6_intf_tentative_address


class TestGetIpv6IntfTentativeAddress(unittest.TestCase):

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

    def test_get_ipv6_intf_tentative_address(self):
        result = get_ipv6_intf_tentative_address(self.device, 'Ethernet0/0')
        expected_output = ['6 is tentative','2001::1']
        self.assertEqual(result, expected_output)
