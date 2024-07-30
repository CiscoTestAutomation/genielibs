import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.aaa.configure import configure_mab_eap_on_switchport_mode_access_interface


class TestConfigureMabEapOnSwitchportModeAccessInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9400-ha:
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
        self.device = self.testbed.devices['9400-ha']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_mab_eap_on_switchport_mode_access_interface(self):
        result = configure_mab_eap_on_switchport_mode_access_interface(self.device, 'TenGigabitEthernet1/2/0/2')
        expected_output = None
        self.assertEqual(result, expected_output)
