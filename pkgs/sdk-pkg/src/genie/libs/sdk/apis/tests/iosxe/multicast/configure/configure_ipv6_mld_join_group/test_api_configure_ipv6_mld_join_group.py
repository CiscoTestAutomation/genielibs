import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_ipv6_mld_join_group


class TestConfigureIpv6MldJoinGroup(unittest.TestCase):

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

    def test_configure_ipv6_mld_join_group(self):
        result = configure_ipv6_mld_join_group(self.device, 'FF08::10', ' gi0/0')
        expected_output = None
        self.assertEqual(result, expected_output)
