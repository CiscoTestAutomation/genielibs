import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_clear_platform_software_fed_switch_acl_counters_hardware


class TestExecuteClearPlatformSoftwareFedSwitchAclCountersHardware(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          h2_svl_9300S:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['h2_svl_9300S']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_platform_software_fed_switch_acl_counters_hardware(self):
        result = execute_clear_platform_software_fed_switch_acl_counters_hardware(self.device, 1)
        expected_output = None
        self.assertEqual(result, expected_output)
