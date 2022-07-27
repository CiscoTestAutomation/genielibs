import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import enable_switchport_trunk_on_interface


class TestEnableSwitchportTrunkOnInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          stack-12m:
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
        self.device = self.testbed.devices['stack-12m']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_enable_switchport_trunk_on_interface(self):
        result = enable_switchport_trunk_on_interface(self.device, 'TenGigabitEthernet10/1/3')
        expected_output = None
        self.assertEqual(result, expected_output)
