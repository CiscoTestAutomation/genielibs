import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import configure_switchport_trunk_pruning_vlan


class TestConfigureSwitchportTrunkPruningVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Skyfox:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Skyfox']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_switchport_trunk_pruning_vlan(self):
        result = configure_switchport_trunk_pruning_vlan(self.device, 'HundredGigE1/0/5', '3')
        expected_output = None
        self.assertEqual(result, expected_output)
