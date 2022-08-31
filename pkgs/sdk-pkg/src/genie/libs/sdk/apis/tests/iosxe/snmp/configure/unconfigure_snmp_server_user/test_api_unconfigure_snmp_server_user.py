import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.snmp.configure import unconfigure_snmp_server_user


class TestUnconfigureSnmpServerUser(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          csr:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: None
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['csr']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_snmp_server_user(self):
        result = unconfigure_snmp_server_user(self.device, 'privuser256256', 'privgrp', 'v3', 'sha-2', '256', 'cisco256', 'aes', '256', 'cisco256', 'ram', 'ipv6', 'nameacl')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_server_user_1(self):
        result = unconfigure_snmp_server_user(self.device, 'privuser256256', 'privgrp', 'v3', 'sha-2', '256', 'cisco256', 'aes', '256', 'cisco256', 'ram', None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_server_user_2(self):
        result = unconfigure_snmp_server_user(self.device, 'privuser256256', 'privgrp', 'v3', 'sha-2', '256', 'cisco256', None, None, None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_unconfigure_snmp_server_user_3(self):
        result = unconfigure_snmp_server_user(self.device, 'privuser256256', 'privgrp', 'v3', None, None, None, None, None, None, None, None, None)
        expected_output = None
        self.assertEqual(result, expected_output)
