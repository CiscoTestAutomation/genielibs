import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.sisf.get import get_ip_theft_syslogs


class TestGetIpTheftSyslogs(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          SISF-C9500-1:
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
        self.device = self.testbed.devices['SISF-C9500-1']
        self.device.connect()

    def test_get_ip_theft_syslogs(self):
        result = get_ip_theft_syslogs(self.device)
        expected_output = {'entries': [{'ip': '2001:DB8::105',
              'mac': 'dead.beef.0001',
              'new_interface': 'Twe1/0/1',
              'vlan': '20'}]}
        self.assertEqual(result, expected_output)
