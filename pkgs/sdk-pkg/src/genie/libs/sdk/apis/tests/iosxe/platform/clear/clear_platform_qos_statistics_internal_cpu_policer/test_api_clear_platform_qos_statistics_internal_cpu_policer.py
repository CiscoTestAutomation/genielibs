import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.clear import clear_platform_qos_statistics_internal_cpu_policer


class TestClearPlatformQosStatisticsInternalCpuPolicer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SG-SVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9600
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SG-SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_platform_qos_statistics_internal_cpu_policer(self):
        result = clear_platform_qos_statistics_internal_cpu_policer(self.device, None, '1')
        expected_output = None
        self.assertEqual(result, expected_output)
