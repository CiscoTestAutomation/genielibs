import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipv6.configure import unconfigure_ipv6_nd_cache_expire


class TestUnconfigureIpv6NdCacheExpire(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9500_STND_1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9500_STND_1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ipv6_nd_cache_expire(self):
        result = unconfigure_ipv6_nd_cache_expire(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
