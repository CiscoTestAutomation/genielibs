import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.debug.configure import debug_platform_memory_fed_callsite


class TestDebugPlatformMemoryFedCallsite(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          stack3-1-3Q-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9300
            type: cat9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack3-1-3Q-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_debug_platform_memory_fed_callsite(self):
        result = debug_platform_memory_fed_callsite(self.device, 'stop', '1', None)
        expected_output = None
        self.assertEqual(result, expected_output)
