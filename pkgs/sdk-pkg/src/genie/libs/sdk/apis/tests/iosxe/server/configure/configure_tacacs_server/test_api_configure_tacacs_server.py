import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.server.configure import configure_tacacs_server


class TestConfigureTacacsServer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Router:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c8kv
            type: c8kv
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Router']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_tacacs_server(self):
        result = configure_tacacs_server(self.device, [{'host': 'TACACS1',
  'key': 'test',
  'key_type': 0,
  'server': '2.2.2.2',
  'timeout': 10}])
        seen = set()
        result_lines = []
        for line in result.splitlines():
            line = line.strip()
            if line and line not in seen:
                seen.add(line)
                result_lines.append(line)
        
        result_normalized = '\n'.join(result_lines) + '\n'

        expected_output = (
            'tacacs server TACACS1\n'
            'address ipv4 2.2.2.2\n'
            'timeout 10\n'
            'key 0 test\n'
            'exit\n'
        )

        self.assertEqual(result_normalized, expected_output)
