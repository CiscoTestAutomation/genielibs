import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import unconfigure_interface_switchport_access_vlan


class TestUnconfigureInterfaceSwitchportAccessVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-21-8-26-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: ios
            type: ios
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-21-8-26-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_interface_switchport_access_vlan(self):
        result = unconfigure_interface_switchport_access_vlan(self.device, 'te1/0/1', 251)
        expected_output = None
        self.assertEqual(result, expected_output)
