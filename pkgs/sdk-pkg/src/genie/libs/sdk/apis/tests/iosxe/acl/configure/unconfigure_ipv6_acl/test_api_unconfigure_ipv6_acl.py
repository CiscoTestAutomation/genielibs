import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.configure import unconfigure_ipv6_acl


class TestUnconfigureIpv6Acl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Int_HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500H
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Int_HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ipv6_acl(self):
        result = unconfigure_ipv6_acl(self.device, 'A-scale6')
        expected_output = None
        self.assertEqual(result, expected_output)
