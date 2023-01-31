import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.bfd.configure import disable_bfd_on_isis_ipv6_address


class TestDisableBfdOnIsisIpv6Address(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          mac-gen2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_disable_bfd_on_isis_ipv6_address(self):
        result = disable_bfd_on_isis_ipv6_address(self.device, 'vlan101')
        expected_output = None
        self.assertEqual(result, expected_output)
