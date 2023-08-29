import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.clear import platform_software_fed_punt_cpuq_clear


class TestPlatformSoftwareFedPuntCpuqClear(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          SKYFOX-DUT3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: C9500
            type: C9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['SKYFOX-DUT3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_platform_software_fed_punt_cpuq_clear(self):
        result = platform_software_fed_punt_cpuq_clear(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
