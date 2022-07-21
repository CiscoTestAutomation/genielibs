import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.snmp.configure import unconfigure_snmp_server_group


class TestUnconfigureSnmpServerGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          UUT:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['UUT']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_snmp_server_group(self):
        result = unconfigure_snmp_server_group(self.device, 'snmp_group', 'v3', 'auth', None, None, None, None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_server_group_1(self):
        result = unconfigure_snmp_server_group(self.device, 'snmp_group', 'v3', 'auth', None, 'useracl', None, 'ipv6', None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_server_group_2(self):
        result = unconfigure_snmp_server_group(self.device, 'snmp_group', 'v3', 'auth', 'read', 'useracl', 'readwrite', 'ipv6', None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_server_group_3(self):
        result = unconfigure_snmp_server_group(self.device, 'snmp_group', 'v3', 'auth', None, None, None, None, 'context', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_server_group_4(self):
        result = unconfigure_snmp_server_group(self.device, 'snmp_group', 'v3', 'auth', None, None, None, None, None, 'exact', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_server_group_5(self):
        result = unconfigure_snmp_server_group(self.device, 'snmp_group', 'v3', 'auth', None, 'useracl', None, None, None, None, 'notify')
        expected_output = None
        self.assertEqual(result, expected_output)
