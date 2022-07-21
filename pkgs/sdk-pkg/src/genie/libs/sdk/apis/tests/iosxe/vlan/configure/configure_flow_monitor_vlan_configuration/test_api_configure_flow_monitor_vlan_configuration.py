import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import configure_flow_monitor_vlan_configuration


class TestConfigureFlowMonitorVlanConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          STARTEK:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['STARTEK']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_flow_monitor_vlan_configuration(self):
        result = configure_flow_monitor_vlan_configuration(self.device, 100, 'fl_mon_Po', 's4', 'input')
        expected_output = None
        self.assertEqual(result, expected_output)
