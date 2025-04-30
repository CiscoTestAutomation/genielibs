import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.snmp.configure import configure_snmp_server_user


class TestConfigureSnmpServerUser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          C1113-8P_pkumarmu:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['C1113-8P_pkumarmu']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_snmp_server_user(self):
        result = configure_snmp_server_user(self.device, 'snmp_user', 'snmp_group', 'v3', 'sha-2', '256', 'cisco123', 'aes', '256', 'cisco123', None, None, None, None, None)
        expected_output = "snmp-server user snmp_user snmp_group v3 auth sha-2 256 cisco123 priv aes 256 cisco123"
        self.assertIn(expected_output, result)

    def test_configure_snmp_server_user_3des(self):
      result = configure_snmp_server_user(self.device, 'snmp_user_3des', 'snmp_group', 'v3', 'sha-2', '256', 'cisco123', '3des', None, None, 256, 'cisco123', None, None, None)
      expected_output = "snmp-server user snmp_user_3des snmp_group v3 auth sha-2 256 cisco123 priv 3des 256 cisco123"
      self.assertIn(expected_output, result)
