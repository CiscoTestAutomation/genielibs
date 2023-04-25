import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.snmp.get import get_snmp_snmpget


class TestGetSnmpSnmpget(unittest.TestCase):

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

    def test_get_snmp_snmpget(self):
        result = get_snmp_snmpget(self.device, 'cisco123', '172.20.249.11', '1.3.6.1.2.1.47.1.1.1.1.11.1', '2c', None)
        expected_output = 'SNMPv2-SMI::mib-2.47.1.1.1.1.11.1 = STRING: "FOC2628Y2N7"'
        self.assertEqual(result, expected_output)
