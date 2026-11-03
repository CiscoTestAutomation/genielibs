import os
import unittest
from unittest.mock import Mock
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.snmp.configure import unconfigure_snmp_host_version


class TestUnconfigureSnmpHostVersion(unittest.TestCase):

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

    def test_unconfigure_snmp_host_version(self):
        result = unconfigure_snmp_host_version(self.device, '172.21.226.240', 'Mgmt-vrf', 'v3', 'public', 10001)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_host_version_with_security_level(self):
        device = Mock()
        unconfigure_snmp_host_version(
            device, '10.1.1.1', 'Mgmt-vrf', version_id='v3',
            community_string='snmpuser1', security_level='priv'
        )
        device.configure.assert_called_once_with(
            'no snmp-server host 10.1.1.1 vrf Mgmt-vrf version v3 priv snmpuser1'
        )

    def test_unconfigure_snmp_host_version_security_level_crlf_rejected(self):
        device = Mock()
        with self.assertRaises(ValueError):
            unconfigure_snmp_host_version(
                device, '10.1.1.1', 'Mgmt-vrf', version_id='v3',
                community_string='snmpuser1', security_level='priv\nmalicious'
            )
