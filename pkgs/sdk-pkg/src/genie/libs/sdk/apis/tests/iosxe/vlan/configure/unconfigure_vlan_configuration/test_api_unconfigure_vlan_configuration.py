import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.configure import unconfigure_vlan_configuration


class TestUnconfigureVlanConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          C9404R_HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C9404R_HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_vlan_configuration(self):
        result = unconfigure_vlan_configuration(self.device, 55)
        expected_output = None
        self.assertEqual(result, expected_output)
