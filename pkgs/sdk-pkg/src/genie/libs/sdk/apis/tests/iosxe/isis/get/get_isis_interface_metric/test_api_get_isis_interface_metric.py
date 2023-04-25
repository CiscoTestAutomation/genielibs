import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.isis.get import get_isis_interface_metric


class TestGetIsisInterfaceMetric(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          iolpe2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['iolpe2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_isis_interface_metric(self):
        result = get_isis_interface_metric(self.device)
        expected_output = [{'interface': 'Loopback1', 'ipv6_metric': 10, 'metric': 10},
 {'interface': 'Tunnel1', 'ipv6_metric': 1, 'metric': 10},
 {'interface': 'Ethernet2/0', 'ipv6_metric': 10, 'metric': 10},
 {'interface': 'Ethernet2/1', 'ipv6_metric': 10, 'metric': 10},
 {'interface': 'Ethernet3/0', 'ipv6_metric': 10, 'metric': 10},
 {'interface': 'Ethernet3/1', 'ipv6_metric': 10, 'metric': 10},
 {'interface': 'Ethernet5/0', 'ipv6_metric': 10, 'metric': 10},
 {'interface': 'Ethernet5/1', 'ipv6_metric': 10, 'metric': 10}]
        self.assertEqual(result, expected_output)
