import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bgp.configure import configure_ospf_redistribute_in_bgp


class TestConfigureOspfRedistributeInBgp(unittest.TestCase):

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

    def test_configure_ospf_redistribute_in_bgp(self):
        result = configure_ospf_redistribute_in_bgp(self.device, 3, 'ipv6', 10, 'internal external 1 external 2', 6, 'test')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ospf_redistribute_in_bgp_1(self):
        result = configure_ospf_redistribute_in_bgp(self.device, 3, 'ipv6', 10, None, 6, 'test')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_ospf_redistribute_in_bgp_2(self):
        result = configure_ospf_redistribute_in_bgp(self.device, 3, 'ipv6', 10, None, None, 'test')
        expected_output = None
        self.assertEqual(result, expected_output)
