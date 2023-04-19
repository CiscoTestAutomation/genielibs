import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_ipv6_mld_join_group_acl


class TestConfigureIpv6MldJoinGroupAcl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          c8kv-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['c8kv-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ipv6_mld_join_group_acl(self):
        result = configure_ipv6_mld_join_group_acl(self.device, 'FF3E:6::1', 'Loopback1', 'ssm_source')
        expected_output = None
        self.assertEqual(result, expected_output)
