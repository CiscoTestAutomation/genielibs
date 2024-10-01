import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.clear import clear_platform_qos_statistics_iif_id


class TestClearPlatformQosStatisticsIifId(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          C9300CR-matrix:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat900
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C9300CR-matrix']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_clear_platform_qos_statistics_iif_id(self):
        result = clear_platform_qos_statistics_iif_id(self.device, 'active', 16777217, 'switch')
        expected_output = None
        self.assertEqual(result, expected_output)
