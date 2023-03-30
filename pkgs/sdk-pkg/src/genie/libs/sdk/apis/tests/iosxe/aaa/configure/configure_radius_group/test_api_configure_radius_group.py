import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_radius_group


class TestConfigureRadiusGroup(unittest.TestCase):

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

    def test_configure_radius_group(self):
        result = configure_radius_group(self.device, {'server_group': 'ISEGRP2'})
        expected_output = ['aaa group server radius ISEGRP2']
        self.assertEqual(result, expected_output)

    def test_configure_radius_group_1(self):
        result = configure_radius_group(self.device, {'dscp_acct': '32', 'dscp_auth': '40', 'server_group': 'ISEGRP2'})
        expected_output = ['aaa group server radius ISEGRP2', 'dscp auth 40', 'dscp acct 32']
        self.assertEqual(result, expected_output)
