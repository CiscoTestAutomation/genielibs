import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.verify import verify_ip_mroute_group_and_sourceip


class TestVerifyIpMrouteGroupAndSourceip(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          leaf1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9300
            type: cat9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['leaf1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_ip_mroute_group_and_sourceip(self):
        result = verify_ip_mroute_group_and_sourceip(self.device, '239.1.1.1', '20.20.20.21', 'ip', 'red', 'FT', 'Vlan100', 'Vlan500', None, [], 30, 10)
        expected_output = True
        self.assertEqual(result, expected_output)
