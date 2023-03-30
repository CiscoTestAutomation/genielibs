import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.l2vpn.configure import configure_evpn_instance_vlan_based_flood_suppression


class TestConfigureEvpnInstanceVlanBasedFloodSuppression(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Leaf-01:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Leaf-01']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_evpn_instance_vlan_based_flood_suppression(self):
        result = configure_evpn_instance_vlan_based_flood_suppression(self.device, '2000')
        expected_output = None
        self.assertEqual(result, expected_output)
