import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.nat.execute import execute_clear_ip_nat_translation


class TestExecuteClearIpNatTranslation(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          stack3-nyquist-1:
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
        self.device = self.testbed.devices['stack3-nyquist-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_clear_ip_nat_translation(self):
        result = execute_clear_ip_nat_translation(self.device, 'GigabitEthernet1/0/3', False, False, '192.168.121.20', '10.10.10.1', '23', '23', '20.20.20.1', '192.168.21.20', '8090', '8090')
        expected_output = '$92.168.121.20 23 outside 20.20.20.1 8090 192.168.21.20 8090'
        self.assertEqual(result, expected_output)
