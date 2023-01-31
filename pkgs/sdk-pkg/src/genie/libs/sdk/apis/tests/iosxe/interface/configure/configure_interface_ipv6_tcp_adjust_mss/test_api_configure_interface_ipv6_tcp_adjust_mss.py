import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_ipv6_tcp_adjust_mss


class TestConfigureInterfaceIpv6TcpAdjustMss(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9200
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_ipv6_tcp_adjust_mss(self):
        result = configure_interface_ipv6_tcp_adjust_mss(self.device, 'gi1/0/6', 900)
        expected_output = None
        self.assertEqual(result, expected_output)
