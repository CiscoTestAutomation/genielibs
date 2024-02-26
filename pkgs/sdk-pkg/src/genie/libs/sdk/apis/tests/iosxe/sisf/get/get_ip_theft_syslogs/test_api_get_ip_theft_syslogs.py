import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.get import get_ip_theft_syslogs


class TestGetIpTheftSyslogs(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-11:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-11']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_ip_theft_syslogs(self):
        result = get_ip_theft_syslogs(self.device)
        expected_output = {'entries': [
            {'ip': '2001:DB8::105',
              'mac': 'dead.beef.0001',
              'new_interface': 'TwentyFiveGigE1/0/1',
              'vlan': '20'},
            {'interface': 'TwentyFiveGigE1/0/1',
              'ip': '2001:DB8::105',
              'mac': 'dead.beef.0001',
              'new_interface': 'TwentyFiveGigE1/0/5',
              'new_mac': 'dead.beef.0002',
              'vlan': '20'},
            {'ip': '2001:DB8::105', 'vlan': '20',
              'new_mac': 'dead.beef.0002',
              'new_interface': 'TwentyFiveGigE1/0/1'},
            {'interface': 'Vlan20',
             'ip': '20.0.0.254',
             'mac': 'ba25.cdf4.ad38',
             'new_interface': 'GigabitEthernet1/0/1',
             'new_mac': 'dead.beef.0002',
             'vlan': '20'}
        ]}

        self.assertEqual(result, expected_output)
