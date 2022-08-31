import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.acl.clear import platform_software_fed_fnf_sw_stats_clear


class TestPlatformSoftwareFedFnfSwStatsClear(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Cat9600-SVL_CGW:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Cat9600-SVL_CGW']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_platform_software_fed_fnf_sw_stats_clear(self):
        result = platform_software_fed_fnf_sw_stats_clear(self.device, '1')
        expected_output = None
        self.assertEqual(result, expected_output)
