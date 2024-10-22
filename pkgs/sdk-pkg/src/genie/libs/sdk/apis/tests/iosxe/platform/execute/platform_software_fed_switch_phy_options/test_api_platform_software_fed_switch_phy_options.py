import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import platform_software_fed_switch_phy_options


class TestPlatformSoftwareFedSwitchPhyOptions(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          hendrix:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: None
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['hendrix']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_platform_software_fed_switch_phy_options(self):
        result = platform_software_fed_switch_phy_options(self.device, 'active', 1, 1, 'read', 0, 0, 0, 0, 0)
        expected_output = (' XcvrPhyRead '
 'Lpn:01,Page:00,DevID:00,Clause:00,Reg:0x0000,Val:0x0000(00):0000 0000 0000 '
 '0000')
        self.assertEqual(result, expected_output)
