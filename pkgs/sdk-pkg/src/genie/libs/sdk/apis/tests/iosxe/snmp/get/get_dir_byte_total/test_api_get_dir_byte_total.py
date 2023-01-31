import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.snmp.get import get_dir_byte_total


class TestGetDirByteTotal(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          n08HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['n08HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_dir_byte_total(self):
        result = get_dir_byte_total(self.device, 'flash:')
        expected_output = {'bytes_free': 6827765760, 'bytes_total': 11353194496}
        self.assertEqual(result, expected_output)
