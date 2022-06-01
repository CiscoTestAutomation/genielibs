import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_trunk_vlan_with_speed_and_duplex


class TestConfigureSwitchportTrunkVlanWithSpeedAndDuplex(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_switchport_trunk_vlan_with_speed_and_duplex(self):
        result = configure_switchport_trunk_vlan_with_speed_and_duplex(self.device, 'GigabitEthernet3/0/25', '3', '10', 'full', 'output', 'test-shape')
        expected_output = None
        self.assertEqual(result, expected_output)
