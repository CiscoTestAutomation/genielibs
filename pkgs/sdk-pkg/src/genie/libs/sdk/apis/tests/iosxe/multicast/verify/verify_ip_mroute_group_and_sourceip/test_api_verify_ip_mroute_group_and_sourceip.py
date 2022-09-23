import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.verify import verify_ip_mroute_group_and_sourceip


class TestVerifyIpMrouteGroupAndSourceip(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          xtr11:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['xtr11']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ip_mroute_group_and_sourceip(self):
        result = verify_ip_mroute_group_and_sourceip(self.device, '239.5.1.100', '70.3.0.2', 'ip', 'VRF2', 'T', 'LISP0.4100', ['Vlan1025', 'LISP0.4101'], None, [], 30, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
