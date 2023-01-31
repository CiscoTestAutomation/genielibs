import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.igmp_snooping.configure import configure_ip_igmp_snooping_vlan_static


class TestConfigureIpIgmpSnoopingVlanStatic(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9300-24UX-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9300-24UX-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ip_igmp_snooping_vlan_static(self):
        result = configure_ip_igmp_snooping_vlan_static(self.device, '200', '225.0.100.100', 'Te1/0/2')
        expected_output = None
        self.assertEqual(result, expected_output)
