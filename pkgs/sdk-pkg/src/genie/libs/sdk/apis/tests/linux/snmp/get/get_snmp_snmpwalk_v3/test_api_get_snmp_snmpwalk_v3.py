import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.linux.snmp.get import get_snmp_snmpwalk_v3


class TestGetSnmpSnmpwalkV3(unittest.TestCase):

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

    def test_get_snmp_snmpwalk_v3(self):
        result = get_snmp_snmpwalk_v3(self.device, '172.20.249.11', '1.3.6.1.4.1.9.9.25.1.1.1.2', 'TestUsr2', 'password1', 'authPriv', 'md5', 'des', 'password', '3', None)
        expected_output = 'snmpget: Unknown user name'
        self.assertEqual(result, expected_output)
