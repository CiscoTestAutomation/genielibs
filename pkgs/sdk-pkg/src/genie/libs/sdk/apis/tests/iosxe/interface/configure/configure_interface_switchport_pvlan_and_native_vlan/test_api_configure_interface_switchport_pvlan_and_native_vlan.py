import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_switchport_pvlan_and_native_vlan


class TestConfigureInterfaceSwitchportPvlanAndNativeVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          core2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['core2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_switchport_pvlan_and_native_vlan(self):
        result = configure_interface_switchport_pvlan_and_native_vlan(self.device, 'twentyFiveGigE 1/0/7', 'trunk', '101')
        expected_output = None
        self.assertEqual(result, expected_output)
