import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ospf.configure import configure_ospf_networks


class TestConfigureOspfNetworks(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ospf_networks(self):
        result = configure_ospf_networks(self.device, 10, ['172.16.70.0', '172.16.71.0', '172.16.80.0'], '0.0.0.255', 0, '1.1.1.1', 'all-interfaces', 'green')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ospf_networks_1(self):
        result = configure_ospf_networks(self.device, 9, ['172.16.70.0', '172.16.71.0', '172.16.80.0'], '0.0.0.255', 0, '1.1.1.1', 'all-interfaces', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ospf_networks_2(self):
        result = configure_ospf_networks(self.device, 5, None, None, None, '1.1.1.1', 'all-interfaces', 'green')
        expected_output = None
        self.assertEqual(result, expected_output)
