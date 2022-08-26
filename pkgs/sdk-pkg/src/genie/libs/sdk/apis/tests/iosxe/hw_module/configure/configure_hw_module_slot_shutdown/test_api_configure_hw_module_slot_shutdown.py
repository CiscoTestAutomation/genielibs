import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.hw_module.configure import configure_hw_module_slot_shutdown


class TestConfigureHwModuleSlotShutdown(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          CR-Vulcan-L25:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['CR-Vulcan-L25']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_hw_module_slot_shutdown(self):
        result = configure_hw_module_slot_shutdown(self.device, '2')
        expected_output = 'hw-module slot 2 shutdown\r\n' \
                          'hw-module slot 2 shutdown\r\n' \
                          '%Shutdown Command is being executed for slot 2\r\n\r\n' \
                          '%Please wait for a minute, before doing any further operations on this card\r\n\r\n'
        self.assertEqual(result, expected_output)
