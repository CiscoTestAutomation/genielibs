import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.snmp.get import get_snmp_snmpwalk_sysname


class TestGetSnmpSnmpwalkSysname(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          vm1-ubuntu1:
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
        self.device = self.testbed.devices['vm1-ubuntu1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_snmp_snmpwalk_sysname(self):
        result = get_snmp_snmpwalk_sysname(self.device, '10.7.21.121', 'SNMPv2-MIB::sysName', 'snmp-poller', 'PASSWORD1', 'authPriv', 'SHA', '/home/vm1/snmp', 'AES', 'PASSWORD1', '3', 'None')
        expected_output = '\r\nSNMPv2-MIB::sysName.0 = STRING: MSFT_9300_LEAF1.cisco.com'
        self.assertEqual(result, expected_output)
