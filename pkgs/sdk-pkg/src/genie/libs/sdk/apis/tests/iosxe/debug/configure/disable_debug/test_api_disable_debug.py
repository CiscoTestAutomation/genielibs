import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.debug.configure import disable_debug


class TestDisableDebug(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          sisf-c9500-22:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['sisf-c9500-22']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_disable_debug(self):
        result = disable_debug(self.device, 'all')
        expected_output = None
        self.assertEqual(result, expected_output)
