import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.stackwise_virtual.configure import configure_global_dual_active_recovery_reload_disable


class TestConfigureGlobalDualActiveRecoveryReloadDisable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          farscape-pinfra-6:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: STARTREK
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['farscape-pinfra-6']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_global_dual_active_recovery_reload_disable(self):
        result = configure_global_dual_active_recovery_reload_disable(self.device)
        expected_output = ('stackwise-virtual\r\n'
 'stackwise-virtual\r\n'
 'dual-active recovery-reload-disable\r\n'
 'Please reload the switch for Stackwise Virtual configuration to take '
 'effect\r\n')
        self.assertEqual(result, expected_output)
