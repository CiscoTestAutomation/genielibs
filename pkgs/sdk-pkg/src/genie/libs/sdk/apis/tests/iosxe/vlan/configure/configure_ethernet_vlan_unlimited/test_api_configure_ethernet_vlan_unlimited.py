import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import configure_ethernet_vlan_unlimited


class TestConfigureEthernetVlanUnlimited(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          BB_1HX:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['BB_1HX']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ethernet_vlan_unlimited(self):
        result = configure_ethernet_vlan_unlimited(self.device, '0/0')
        expected_output = None
        self.assertEqual(result, expected_output)
