import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_switchport_trunk_native_vlan


class TestUnconfigureSwitchportTrunkNativeVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Sup-9600-HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9600
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Sup-9600-HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_switchport_trunk_native_vlan(self):
        result = unconfigure_switchport_trunk_native_vlan(self.device, 'TwentyFiveGigE1/0/37', '501')
        expected_output = None
        self.assertEqual(result, expected_output)
