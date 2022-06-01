import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_diagnostic_start_switch_module_test


class TestExecuteDiagnosticStartSwitchModuleTest(unittest.TestCase):

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

    def test_execute_diagnostic_start_switch_module_test(self):
        result = execute_diagnostic_start_switch_module_test(self.device, 1, 1, 'all')
        expected_output = None
        self.assertEqual(result, expected_output)
