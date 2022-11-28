import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_snooping_last_member_query_interval


class TestUnconfigureIpIgmpSnoopingLastMemberQueryInterval(unittest.TestCase):

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

    def test_unconfigure_ip_igmp_snooping_last_member_query_interval(self):
        result = unconfigure_ip_igmp_snooping_last_member_query_interval(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
