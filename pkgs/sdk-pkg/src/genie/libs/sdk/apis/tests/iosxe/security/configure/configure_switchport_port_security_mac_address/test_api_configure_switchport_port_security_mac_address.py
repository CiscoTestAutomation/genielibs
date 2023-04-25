import os
import unittest
from unittest.mock import NonCallableMock
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.security.configure import configure_switchport_port_security_mac_address


class TestConfigureSwitchportPortSecurityMacAddress(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          n08HA:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['n08HA']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_switchport_port_security_mac_address(self):
        result = configure_switchport_port_security_mac_address(self.device, 'g1/1/1', 'sticky', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_switchport_port_security_mac_address_1(self):
        result = configure_switchport_port_security_mac_address(self.device, 'g1/1/1', '0001.0001.000c', 'voice')
        expected_output = None
        self.assertEqual(result, expected_output)
