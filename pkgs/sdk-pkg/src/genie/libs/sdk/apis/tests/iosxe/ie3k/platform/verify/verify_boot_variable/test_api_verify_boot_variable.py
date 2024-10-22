import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ie3k.platform.verify import verify_boot_variable


class TestVerifyBootVariable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          IE-3300-8U2X-tgen1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ie3k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['IE-3300-8U2X-tgen1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_boot_variable(self):
        result = verify_boot_variable(self.device, 'sdflash:/ie31xx-universalk9.BLD_POLARIS_DEV_LATEST_20240301_003017.SSA.bin', None)
        expected_output = False
        self.assertEqual(result, expected_output)
