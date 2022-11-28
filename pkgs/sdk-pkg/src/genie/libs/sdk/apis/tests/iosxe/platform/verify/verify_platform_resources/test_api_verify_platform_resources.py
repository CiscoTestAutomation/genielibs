import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.verify import verify_platform_resources


class TestVerifyPlatformResources(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IE-3100-8T2C:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: IE-3100-8T2C
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IE-3100-8T2C']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_platform_resources(self):
        result = verify_platform_resources(self.device, '1656', '0', '0', '0', 15, 5)
        expected_output = True
        self.assertEqual(result, expected_output)
