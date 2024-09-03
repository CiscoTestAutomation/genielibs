import os
import unittest
from pyats.topology import loader

import unicon
from unicon.plugins.tests.mock.mock_device_iosxe import MockDeviceTcpWrapperIOSXE

from genie.libs.sdk.apis.iosxe.platform.configure import configure_macro_name

unicon.settings.Settings.POST_DISCONNECT_WAIT_SEC = 0
unicon.settings.Settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0.2


class TestConfigureMacroName(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.md = MockDeviceTcpWrapperIOSXE(
            hostname='C9300CR-matrix',
            port=0, state='connect',
            mock_data_dir=f'{os.path.dirname(__file__)}/mock_data')
        cls.md.start()

        cls.testbed = loader.load("""
        devices:
          C9300CR-matrix:
            os: iosxe
            type: router
            tacacs:
                username: cisco
            passwords:
                tacacs: cisco
            connections:
              defaults:
                class: unicon.Unicon
              a:
                protocol: telnet
                ip: 127.0.0.1
                port: {}
        """.format(cls.md.ports[0]))
        cls.device = cls.testbed.devices['C9300CR-matrix']
        cls.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[],
        )

    @classmethod
    def tearDownClass(cls):
        cls.device.disconnect()
        cls.md.stop()

    def test_configure_macro_name(self):
        result = configure_macro_name(self.device, 'm-qos', ['default interface $interface',
 'interface $interface',
 'description',
 'switchport access vlan 10',
 'switchport mode access',
 '@'], 60)
        expected_output = None
        self.assertEqual(result, expected_output)
