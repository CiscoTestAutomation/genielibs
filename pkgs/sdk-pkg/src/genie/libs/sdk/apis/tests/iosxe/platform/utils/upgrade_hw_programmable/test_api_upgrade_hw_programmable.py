import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.utils import upgrade_hw_programmable


class TestUpgradeHwProgrammable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Dt-6X:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Dt-6X']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_upgrade_hw_programmable(self):
        result = upgrade_hw_programmable(self.device, 'fpga', 'bootflash:', 'asr1000-hw-programmables.16.08.01.SPA.pkg', 'R1')
        expected_output = ('$lename bootflash:asr1000-hw-programmables.16.08.01.SPA.pkg R1\r\n'
 'Start service Upgrade FPGA on Route-Processor 1 from current version '
 '18102401 to 17071402  (Y)es/(N)o/(C)ontinue? [Y')
        self.assertEqual(result, expected_output)
