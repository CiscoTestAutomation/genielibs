import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.snmp.get import get_snmp_snmpwalk_version3


class TestGetSnmpSnmpwalkVersion3(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          morph-full2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os linux --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: linux
            platform: linux
            type: linux
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['morph-full2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_snmp_snmpwalk_version3(self):
        result = get_snmp_snmpwalk_version3(self.device, '172.20.249.11', '1.3.6.1.4.1.9.9.25.1.1.1.2', '3', 'testUsr', '-A', 'password1', '-l', '-a', 'authNoPriv', 'sha', 'des', 'password', None)
        expected_output = ('SNMPv2-SMI::enterprises.9.9.25.1.1.1.2.1 = STRING: '
 '"CW_BEGIN$-gs-universalk9-m$"\r\n'
 'SNMPv2-SMI::enterprises.9.9.25.1.1.1.2.2 = STRING: '
 '"CW_IMAGE$CAT9K_IOSXE$"\r\n'
 'SNMPv2-SMI::enterprises.9.9.25.1.1.1.2.3 = STRING: '
 '"CW_FAMILY$CAT9K_IOSXE$"\r\n'
 'SNMPv2-SMI::enterprises.9.9.25.1.1.1.2.4 = STRING: '
 '"CW_FEATURE$IP|SLA|IPv6|IS-IS|FIREWALL|PLUS|QoS|HA|NAT|MPLS|VPN|LEGACY '
 'PROTOCOLS|3DES|SSH|APPN|IPSEC$"\r\n'
 'SNMPv2-SMI::enterprises.9.9.25.1.1.1.2.5 = STRING: '
 '"CW_VERSION$17.13.20230427:005651$"\r\n'
 'SNMPv2-SMI::enterprises.9.9.25.1.1.1.2.6 = STRING: "CW_MEDIA$RAM$"\r\n'
 'SNMPv2-SMI::enterprises.9.9.25.1.1.1.2.7 = STRING: "CW_SYSDESCR$Cisco IOS '
 'Software [Dublin], Catalyst L3 Switch Software (CAT9K_IOSXE), Experimental '
 'Version 17.13.20230427:005651 '
 '[BLD_POLARIS_DEV_LATEST_20230427_003231:/nobackup/mcpre/s2c-build-ws 101]\r\n'
 'Copyright (c) 1986-2023 by Cisco Systems, Inc.\r\n'
 'Compil+"\r\n'
 'SNMPv2-SMI::enterprises.9.9.25.1.1.1.2.8 = STRING: '
 '"CW_END$-gs-universalk9-m$"')
        self.assertEqual(result, expected_output)
