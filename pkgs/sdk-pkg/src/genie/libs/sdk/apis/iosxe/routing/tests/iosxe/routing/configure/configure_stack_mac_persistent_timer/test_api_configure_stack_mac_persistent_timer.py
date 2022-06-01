import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.configure import configure_stack_mac_persistent_timer


class TestConfigureStackMacPersistentTimer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          startrek-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300X
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['startrek-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_stack_mac_persistent_timer(self):
        result = configure_stack_mac_persistent_timer(self.device, '3')
        expected_output = None
        self.assertEqual(result, expected_output)
