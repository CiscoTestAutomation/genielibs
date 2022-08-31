import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.rip.configure import unconfig_interface_ripng


class TestUnconfigInterfaceRipng(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          core:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['core']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfig_interface_ripng(self):
        result = unconfig_interface_ripng(self.device, 'TwentyFiveGigE1/0/2', '64')
        expected_output = None
        self.assertEqual(result, expected_output)
