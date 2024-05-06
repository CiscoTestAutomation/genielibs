import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_switchport_mode_trunk_snooping_trust


class TestConfigureSwitchportModeTrunkSnoopingTrust(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          rep-sw2:
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
        self.device = self.testbed.devices['rep-sw2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_switchport_mode_trunk_snooping_trust(self):
        result = configure_switchport_mode_trunk_snooping_trust(self.device, {'GigabitEthernet1/0/17': None})
        expected_output = None
        self.assertEqual(result, expected_output)
