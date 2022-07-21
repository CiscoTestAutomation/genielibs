import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_trunk_allowed_vlan


class TestConfigureSwitchportTrunkAllowedVlan(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9300-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_switchport_trunk_allowed_vlan(self):
        result = configure_switchport_trunk_allowed_vlan(self.device, 'TwoGigabitEthernet1/0/3', 10)
        expected_output = None
        self.assertEqual(result, expected_output)
