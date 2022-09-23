import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.snmp.configure import configure_snmp_server_trap


class TestConfigureSnmpServerTrap(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          startrek-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300X
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['startrek-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_snmp_server_trap(self):
        result = configure_snmp_server_trap(self.device, 'HundredGigE1/0/27', '70.70.70.2', 'traps', '3', 'privuser256256', 'config', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_snmp_server_trap_1(self):
        result = configure_snmp_server_trap(self.device, 'HundredGigE1/0/27', '70.70.70.2', 'informs', '3', 'privuser256256', 'config', '800000090300005056BE0829')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_snmp_server_trap_2(self):
        result = configure_snmp_server_trap(self.device, None, None, 'snmp', None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_snmp_server_trap_3(self):
        result = configure_snmp_server_trap(self.device, None, None, '', None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
