import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.evpn.configure import configure_evpn_l2_instance_vlan_association


class TestConfigureEvpnL2InstanceVlanAssociation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          NyqC:
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
        self.device = self.testbed.devices['NyqC']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_evpn_l2_instance_vlan_association(self):
        result = configure_evpn_l2_instance_vlan_association(self.device, '10', '10', '60010')
        expected_output = None
        self.assertEqual(result, expected_output)
