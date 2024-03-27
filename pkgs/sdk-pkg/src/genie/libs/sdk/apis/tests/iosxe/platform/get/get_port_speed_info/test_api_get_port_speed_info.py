import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.get import get_port_speed_info


class TestGetPortSpeedInfo(unittest.TestCase):

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

    def test_get_port_speed_info(self):
        result = get_port_speed_info(self.device)
        expected_output = {'interface': ['TenGigabitEthernet2/3/0/1',
               'TenGigabitEthernet2/3/0/2',
               'TenGigabitEthernet2/3/0/3',
               'TenGigabitEthernet2/3/0/4',
               'TenGigabitEthernet2/3/0/5',
               'TenGigabitEthernet2/3/0/6',
               'TenGigabitEthernet2/3/0/7',
               'TenGigabitEthernet2/3/0/8',
               'FortyGigabitEthernet2/3/0/9',
               'FortyGigabitEthernet2/3/0/10',
               'GigabitEthernet2/7/0/1',
               'GigabitEthernet2/7/0/2',
               'GigabitEthernet2/7/0/3',
               'GigabitEthernet2/7/0/4',
               'GigabitEthernet2/7/0/5',
               'GigabitEthernet2/7/0/6',
               'GigabitEthernet2/7/0/7',
               'GigabitEthernet2/7/0/8',
               'GigabitEthernet2/7/0/9',
               'GigabitEthernet2/7/0/10',
               'GigabitEthernet2/7/0/11',
               'GigabitEthernet2/7/0/12',
               'GigabitEthernet2/7/0/13',
               'GigabitEthernet2/7/0/14',
               'GigabitEthernet2/7/0/15',
               'GigabitEthernet2/7/0/16',
               'GigabitEthernet2/7/0/17',
               'GigabitEthernet2/7/0/18',
               'GigabitEthernet2/7/0/19',
               'GigabitEthernet2/7/0/20',
               'GigabitEthernet2/7/0/21',
               'GigabitEthernet2/7/0/22',
               'GigabitEthernet2/7/0/23',
               'GigabitEthernet2/7/0/24',
               'GigabitEthernet2/7/0/25',
               'GigabitEthernet2/7/0/26',
               'GigabitEthernet2/7/0/27',
               'GigabitEthernet2/7/0/28',
               'GigabitEthernet2/7/0/29',
               'GigabitEthernet2/7/0/30',
               'GigabitEthernet2/7/0/31',
               'GigabitEthernet2/7/0/32',
               'GigabitEthernet2/7/0/33',
               'GigabitEthernet2/7/0/34',
               'GigabitEthernet2/7/0/35',
               'GigabitEthernet2/7/0/36',
               'GigabitEthernet2/7/0/37',
               'GigabitEthernet2/7/0/38',
               'GigabitEthernet2/7/0/39',
               'GigabitEthernet2/7/0/40',
               'GigabitEthernet2/7/0/41',
               'GigabitEthernet2/7/0/42',
               'GigabitEthernet2/7/0/43',
               'GigabitEthernet2/7/0/44',
               'GigabitEthernet2/7/0/45',
               'GigabitEthernet2/7/0/46',
               'GigabitEthernet2/7/0/47',
               'GigabitEthernet2/7/0/48'],
 'port_speed': ['openconfig-if-ethernet:SPEED_10GB',
                'openconfig-if-ethernet:SPEED_10GB',
                'openconfig-if-ethernet:SPEED_10GB',
                'openconfig-if-ethernet:SPEED_10GB',
                'openconfig-if-ethernet:SPEED_10GB',
                'openconfig-if-ethernet:SPEED_10GB',
                'openconfig-if-ethernet:SPEED_10GB',
                'openconfig-if-ethernet:SPEED_10GB',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_1GB',
                'openconfig-if-ethernet:SPEED_1GB',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_UNKNOWN',
                'openconfig-if-ethernet:SPEED_1GB']}
        self.assertEqual(result, expected_output)
