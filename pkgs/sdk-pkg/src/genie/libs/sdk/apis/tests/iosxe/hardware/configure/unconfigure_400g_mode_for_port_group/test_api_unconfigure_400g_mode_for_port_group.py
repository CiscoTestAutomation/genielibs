import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.hardware.configure import unconfigure_400g_mode_for_port_group


class TestUnconfigure400gModeForPortGroup(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: Switch
            type: Switch
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_400g_mode_for_port_group(self):
        result = unconfigure_400g_mode_for_port_group(self.device, '2', '2')
        expected_output = None
        self.assertEqual(result, expected_output)
