import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import unconfigure_ip_igmp_snooping_vlan_mrouter_interface


class TestUnconfigureIpIgmpSnoopingVlanMrouterInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ip_igmp_snooping_vlan_mrouter_interface(self):
        result = unconfigure_ip_igmp_snooping_vlan_mrouter_interface(self.device, 100, 'Gi1/0/10')
        expected_output = None
        self.assertEqual(result, expected_output)
