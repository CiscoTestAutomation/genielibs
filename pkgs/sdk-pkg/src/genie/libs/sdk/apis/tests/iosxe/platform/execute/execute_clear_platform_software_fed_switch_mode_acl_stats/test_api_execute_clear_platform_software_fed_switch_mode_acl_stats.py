import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_clear_platform_software_fed_switch_mode_acl_stats


class TestExecuteClearPlatformSoftwareFedSwitchModeAclStats(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Intrepid-DUT-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9600
            type: C9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Intrepid-DUT-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_platform_software_fed_switch_mode_acl_stats(self):
        result = execute_clear_platform_software_fed_switch_mode_acl_stats(device=self.device, switch_mode='active')
        expected_output = None
        self.assertEqual(result, expected_output)
