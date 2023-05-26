import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_switchport_trunk_allowed_vlan


class TestUnconfigureInterfaceSwitchportTrunkAllowedVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          A1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['A1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_interface_switchport_trunk_allowed_vlan(self):
        result = unconfigure_interface_switchport_trunk_allowed_vlan(self.device, ['po 10'], '10-30,499,777')
        expected_output = None
        self.assertEqual(result, expected_output)
