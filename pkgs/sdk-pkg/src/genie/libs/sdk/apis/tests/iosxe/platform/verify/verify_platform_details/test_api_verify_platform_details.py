import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.verify import verify_platform_details


class TestVerifyPlatformDetails(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          1783-CMS20DN:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: s5k
            type: switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['1783-CMS20DN']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_platform_details(self):
        result = verify_platform_details(self.device, '03', 'acbc.d937.9d40', '1783-CMS20DN', '20', '1', 'FDO2607J4SK', '17.10.01', 15, 5)
        expected_output = True
        self.assertEqual(result, expected_output)
