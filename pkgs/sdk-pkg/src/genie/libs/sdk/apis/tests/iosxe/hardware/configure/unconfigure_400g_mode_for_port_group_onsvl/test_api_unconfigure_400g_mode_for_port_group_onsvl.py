import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.hardware.configure import unconfigure_400g_mode_for_port_group_onsvl


class TestUnconfigure400gModeForPortGroupOnsvl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          NG_SVL_AUT1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: INTREPID
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['NG_SVL_AUT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_400g_mode_for_port_group_onsvl(self):
        result = unconfigure_400g_mode_for_port_group_onsvl(self.device, 2, 2, '1-2', None)
        expected_output = None
        self.assertEqual(result, expected_output)
