import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.vlan.get import get_vlan_name_status


class TestGetVlanNameStatus(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          HA-9400-S2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['HA-9400-S2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_vlan_name_status(self):
        result = get_vlan_name_status(self.device)
        expected_output = {'vlan_id': ['1',
             '2',
             '4',
             '5',
             '10',
             '12',
             '20',
             '30',
             '40',
             '55',
             '68',
             '100',
             '101',
             '200',
             '300',
             '1002',
             '1003',
             '1004',
             '1005'],
 'vlan_name': ['default',
               'VLAN0002',
               'VLAN0004',
               'VLAN0005',
               'VLAN0010',
               'VLAN0012',
               'VLAN0020',
               'VLAN0030',
               'VLAN0040',
               'VLAN0055',
               'VLAN0068',
               'VLAN0100',
               'VLAN0101',
               'VLAN0200',
               'VLAN0300',
               'fddi-default',
               'trcrf-default',
               'fddinet-default',
               'trbrf-default'],
 'vlan_state': ['ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'ACTIVE',
                'SUSPENDED',
                'SUSPENDED',
                'SUSPENDED',
                'SUSPENDED'],
 'vrf': ['default',
         'default',
         'default',
         'default',
         'vrf_10',
         'default',
         'default',
         'default',
         'default',
         'default',
         'default',
         'default',
         'default',
         'default',
         'blue',
         'default',
         'default',
         'default',
         'default']}
        self.assertEqual(result, expected_output)
