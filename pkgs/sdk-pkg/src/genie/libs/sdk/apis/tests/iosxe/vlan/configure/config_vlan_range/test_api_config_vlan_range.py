import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import config_vlan_range


class TestConfigVlanRange(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          mac-gen2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_vlan_range(self):
        result = config_vlan_range(device=self.device, vlanid_start='1', vlanid_end='4094')
        expected_output = None
        self.assertEqual(result, expected_output)
