import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.arp.configure import configure_arp_access_list_permit_ip_host


class TestConfigureArpAccessListPermitIpHost(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          n08HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['n08HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_arp_access_list_permit_ip_host(self):
        result = configure_arp_access_list_permit_ip_host(self.device, 'allowed_acl', 'permit', '10.1.1.1', 'any', True)
        expected_output = None
        self.assertEqual(result, expected_output)
