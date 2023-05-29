import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.eigrp.configure import shutdown_ipv6_eigrp_instance


class TestShutdownIpv6EigrpInstance(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          ACE:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ASR1K
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ACE']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_shutdown_ipv6_eigrp_instance(self):
        result = shutdown_ipv6_eigrp_instance(self.device, 1)
        expected_output = None
        self.assertEqual(result, expected_output)
